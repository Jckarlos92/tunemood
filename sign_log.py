import re
from handler import Handler
from google.appengine.api import mail
import hmac
from tables import User


SECRET = "tunemood_app"
EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
PASS_RE = re.compile(r"^.{3,20}$")

def valid_password(password):
    return password and PASS_RE.match(password)

def valid_email(email):
    return not email or EMAIL_RE.match(email)

def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

#obtener por email un User
def by_email(email):
    u = User.all().filter("email =", email).get()
    return u

#obtener por link generado un User
def by_lg(link):
    u = User.all().filter("link_generated =", link).get()
    return u

#funcion para generar la cookie
def make_secure_val(s):
    return "%s|%s"%(s, hash_str(s))

#checar que la cookie coincida
def check_secure_val(h):
    """
    h: string of format: string|HASH
    returns: string part of given string
    """
    v = h.rsplit('|')[0]
    if h == make_secure_val(v):
        return v

class SignUp(Handler):

    def post(self):
        self.email = self.request.get("email_up")
        self.pass_up = self.request.get("password_up")
        self.repass_up = self.request.get("re_password_up")

        have_error = False

        #validaciones de email, password
        if not valid_email(self.email):
            self.response.out.write("Your email is not valid")
            have_error = True

        if not valid_password(self.pass_up) or not valid_password(self.repass_up) and not have_error:
            self.response.out.write("Your password is invalid")
            have_error = True

        if self.pass_up != self.repass_up and not have_error:
            have_error = True

        #mandar email
        if not have_error:

            self.confirmation_link = "http://www.tunnymood.appspot.com/lg=" + hash_str(self.email)
            sender_address = "TuneMood <pedrotrens@gmail.com>"
            subject = "Confirm Your Registration"
            body = "Welcome to TuneMood, click on the link to finish your registration \n %s" % self.confirmation_link

            mail.send_mail(sender_address, self.email, subject, body)
            self.register()

    #registrar el usuario en la base de datos
    def register(self):

        u = by_email(self.email)

        #si el usuario ya existe
        if u:
            self.response.out.write("User Already Exists")
        else:
            user = User(email=self.email,
                        hash_pw=hash_str(self.pass_up),
                        link_generated=self.confirmation_link)

            user.put()#guarda en la base de datos el usuario creado
            self.response.out.write("An confirmation email was sent to your account")


class Confirmation(Handler):

    def get(self):

        link = self.request.get("lg")
        user = by_lg(link)

        if user:
            user.is_user = True
            hashed_user = make_secure_val(str(user.key().id()))
            self.response.headers.add_header('Set-Cookie', 'user_id = %s; path=/'%hashed_user)
            self.redirect('/')





