HAI

WAZZUP
    I HAS A age
    I HAS A hasID
    I HAS A approved
BUHBYE

VISIBLE "Enter age: "
GIMMEH age
age IS NOW A NUMBAR

BOTH SAEM age AN BIGGR OF age AN 18
O RLY?
    YA RLY
        VISIBLE "Age requirement satisfied"

        VISIBLE "Do you have an ID? (Y/N)"
        GIMMEH hasID

        BOTH SAEM hasID AN "Y"
        O RLY?
            YA RLY
                VISIBLE "ID verified"

                VISIBLE "Are you approved? (Y/N)"
                GIMMEH approved

                BOTH SAEM approved AN "Y"
                O RLY?
                    YA RLY
                        VISIBLE "Access granted"
                    NO WAI
                        VISIBLE "Access denied: Not approved"
                OIC

            NO WAI
                VISIBLE "Access denied: No ID"
        OIC

    NO WAI
        VISIBLE "Access denied: Age requirement"
OIC

KTHXBYE

