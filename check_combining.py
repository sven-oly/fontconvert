# https://www.google.com/search?q=unicode+property+combining+characters&rlz=1C5OZZY_en&gs_lcrp=EgZjaHJvbWUqBwgBECEYoAEyBggAEEUYOTIHCAEQIRigATIHCAIQIRigATIHCAMQIRifBTIHCAQQIRifBTIHCAUQIRifBTIHCAYQIRifBTIHCAcQIRifBTIHCAgQIRifBTIHCAkQIRifBdIBCTEwMjYxajBqN6gCALACAA&sourceid=chrome&ie=UTF-8&fbs=ABfTbFVyMZGZf1hfvX9uKjN_-G8c4u0nXx4bEIpwm1lnNH832a9BVCEiB2iPJNekNderQwLP8msUKsz-6AMxGyueJZ9cK2mNBy2II_6WvkKSZWdegvvKnEPeeArWgEP9exNATg6oybL0Q4MEKOxPxFbct-gPoxJydwQkFVgNkm6vNXPQZjfoWDOyzkktih_Z6lssQmfbdqIKqxUyGROmvXoo-iyz5AhpVQ&aep=10&ntc=1&sxsrf=APpeQntNQsl0Q61QNTK7ehRzKA7KiDHnIA%3A1791084039410&mstk=AUtExfD6JWOB_DJBa-tbzL4VQFQqul4Na9fbAfklKsuyv35WTGMpTi2VbsrLMhOgmD7WBgPrVXKtOk4IBi9BqscqlZF6gzEaGnOFepAo1EI0FB52V82oCsratJVVNrjnljYUzMS-NUsLyaegqhZuWaHDf_zGeyWh8GeGnOZfth3rXcNev_W_4OexUnjHvg9z3d3BE5uffh-zyJzFSvB2dvs0hrJ8kVj6C22hZNCe_m7yTfsh-8EDMl9kW6uXYzBSfR5qep2bgB6RCLfY4Fow4YOKmaAwYsGXA_pWcweGxIDbppOMnfXwHlnBLAzX5__UC9Wg090FnPYEFot1MFGQEwkXD-LWF91Y1YEg2dDkIHgR-Tz9qgKBjboaWj0ZW_a-CKDsuLUBxiue68FvIVhRITv0mKD4JdPTYPiB5Q&aioh=3&csuir=1&cs=0&udm=50&mtid=WMbBaqe5JaqfkPIPlJGG6A4&cq=Handle+unicode+property+combining+characters+in+python&zx=1791084123772

# Check the cateogory of a character
import unicodedata

import sys
def test_chars():

    # Examples: 'a' (Base), '◌́' (Combining Acute Accent)
    char1 = 'a'
    char2 = '\u0301'
    char3 = '\u1031'
    chars = [char1, char2, char3, '\u103c', '\u103d', '\u103e']

    for code_point in chars:
        print(f"'{code_point}': {unicodedata.category(code_point)}")  # Output: 'Ll' (Letter, lowercase)
        print (f"    combining order ={unicodedata.combining(code_point)}")

        # Check if a character is any type of combining mark
        print(f"      {code_point} starts with 'M': = {unicodedata.category(code_point).startswith('M')}")


def main(argv):
    test_chars()


if __name__ == '__main__':
    main(sys.argv)
