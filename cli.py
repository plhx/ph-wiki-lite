import argparse
import binascii
from wiki.services import *
from wiki.application.password_getall import *
from wiki.application.password_add import *
from wiki.application.password_remove import *
from wiki.application.password_purge import *
from wiki.domain.models.password import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-a', '--add', type=str)
    parser.add_argument('-r', '--remove', type=str)
    parser.add_argument('-p', '--purge', action='store_true')
    args = parser.parse_args()
    if args.list:
        request = PasswordGetAllRequest()
        response = Service.call(request)
        for i, password in enumerate(response.passwords):
            print('[{}]: {{value: {}, secret: {}}}'.format(
                i,
                password.value,
                binascii.hexlify(password.secret.value)
            ))
    elif args.add:
        request = PasswordAddRequest(Password(args.add))
        response = Service.call(request)
    elif args.remove:
        request = PasswordGetAllRequest()
        response = Service.call(request)
        for password in response.passwords:
            if args.remove == password.value:
                Service.call(PasswordRemoveRequest(password))
    elif args.purge:
        request = PasswordPurgeRequest()
        Service.call(request)
