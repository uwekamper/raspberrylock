import base64
import hashlib
import logging

import ldap3

from .base_authorization import BaseAuthorization

log = logging.getLogger(__name__)


class CBaseLDAPAuthorization(BaseAuthorization):

    def check_c_base_hash(self, record, pin, username):
        bd = base64.b64decode(bytearray(record[6:], 'UTF-8'))
        hash = hashlib.sha1(bytearray(pin, 'UTF-8') + bd[20:]).digest()
        if bd[:20] == hash:
            log.info('login successful for user %s' % username)
            return True
        else:
            log.warning('login failed, PIN incorrect')
            return False

    def check(self, uid: str, pin: str) -> bool:
        """
        Check the ldap if the given uid and pin is valid.
        :param uid: The c-base user id (numerical)
        :param pin: The PIN entered by the user via the keyboard
        :return: True if user should be allowed in, false otherwise
        """
        if uid == '' or pin == '':
            return False

        try:
            server = ldap3.Server(self.config.URI, get_info=ldap3.ALL)
            with ldap3.Connection(server, self.config.BINDDN, self.config.BINDPW,
                                  auto_bind=True) as conn:
                conn.search(self.config.BASE,
                           self.config.ACCESS_FILTER.format(uid),
                           attributes=['uid', 'c-labPIN'])
                if len(conn.entries) > 0:
                    username = conn.entries[0]['uid'].value
                    record = conn.entries[0]['c-labPIN'].value

                    # This should never work, but maybe there are some legacy LDAP entries that
                    # are not hashed.
                    if record == pin:
                        return True

                    # In the default case, PINs in the c-base LDAP are stored as hashes
                    elif record != None and record.startswith('{SSHA}'):
                        checked_hash = self.check_c_base_hash(record, pin, username)
                        log.info("Check returned {}".format(checked_hash))

                        if checked_hash == True:
                            return True
                    else:
                        log.error('PIN incorrectly stored in LDAP, please re-enter PIN.')

                else:
                    log.warning('UID not found, checking guests')
                    #return self.check_guest(uid, pin)
                    # TODO: Add guests
                    return False
        except Exception as e:
            log.error('ldap connection failed: %s' % e)
        finally:
            return False