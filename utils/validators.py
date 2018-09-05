import re


class Validators:
    def valid_name(self, username):
        """ Valid username """
        return re.match("^[a-zA-Z0-9]{6,}$", username)

    def valid_password(self, password):
        """validate for password """
        # positive look ahead
        return re.match("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[a-zA-Z0-9]{8,15}$",
                        password)

    def valid_email(self, email):
        """ validate for email """
        return re.match("^[^@]+@[^@]+\.[^@]+$", email)

    def valid_inputs(self, string_inputs):
        """ validate for inputs """
        # return re.match("^[a-zA-Z0-9-\._@ ]+$", string_inputs)
        return re.match("^[a-zA-Z0-9-\._@ ]+$", string_inputs)

    def valid_is_admin(self, is_admin):
        """ validate is_admin """
        return re.match("^[0-1]{,1}$", is_admin)

    def valid_price(self, price):
        """ validate price """
        return re.match("^[0-9]{3,6}$", price)
