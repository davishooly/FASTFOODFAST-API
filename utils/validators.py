# module import
import re


class Validators:
    def valid_name(self, username):
        """ Valid username """
        return re.match("^[a-zA-Z]+$", username)

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
        return re.match("^[a-zA-Z0-9-\._@]+$", string_inputs)
