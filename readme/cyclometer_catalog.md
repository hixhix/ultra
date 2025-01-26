# Cyclometer Catalog

When an operator is setting up a Wehrmacht Enigma Machine they must create a random three letter message key.
The machine procedure requires that the operator double encipher the message key. For example the ground settings
in the key sheet is FQY every operator sets the Rotor Settings to FQY. Each operator then creates there own random 
three letter message key for example XYZ and will enter it into the enigma machine twice to double encipher it which 
may produce PKYALI. The operator then sets the Rotor Settings to XYZ to encrypt the message. The double enciphered 
message key PKYALI is sent with the encrypted message.

The recieving operator will set there enigma machine up with the same Rotor Settings from the key sheet. With 
the Rotor Settings set to FQY the recieving operator will input the first six letters in the recieved cipher text 
PKYALI and get XYZXYZ. The recieving operator will now set the Rotor Settings to XYZ and decrypt the rest of the 
cipher text.

Marian Rejewski of the Polish Cipher Bureau came up with the idea of cycles in the double enciphered message keys.
Rejewski divided the double enciphered keys into three groups which we will call G1,G2,G3. In the six character
double enciphered key Group 1 G1 is the 1st and 4th character, Group 2 G2 is the 2nd and 5th character, Group 3 G3 
is the 3rd and 6th character.

```
CYCLE 1

ABCDEFGHIJKLMNOPQRSTUVWXYZ

ANJKBC
KHLRGW
RAPZVD
ZUGXZJ
XNKHBP
HDNMIE
MPCAYO

AKRZXHMA


CYCLE 2

ABCDEFGHIJKLMNOPQRSTUVWXYZ
-      -  - -    -     - -

BXFSPM
SQWPRR
PLRDDG
DNHVBI
VYHBQI

BSPDVB


CYCLE 3

ABCDEFGHIJKLMNOPQRSTUVWXYZ
-- -   -  - -  - --  - - -

CSJNOC
NSOUOS
UWROMG
OLOEDS
EBPIED
IBHLEI
LEQCNU

CNUOEILC


CYCLE 4

ABCDEFGHIJKLMNOPQRSTUVWXYZ
-----  -- ------ -- -- - -

FYITQL
TPDJYN
JBGWEJ
WPNYYE
YJDFFN

FTJWYF


CYCLE 5

ABCDEFGHIJKLMNOPQRSTUVWXYZ
------ --------- ---------

GASGVQ

GG


CYCLE 6

ABCDEFGHIJKLMNOPQRSTUVWXYZ
---------------- ---------

QQBQRA

QQ


CYCLE 7

ABCDEFGHIJKLMNOPQRSTUVWXYZ
--------------------------

G1 (AKRZXHM)(BSPDV)(CNUOEIL)(FTJWY)(G)(Q)

G1 (7)(5)(7)(5)(1)(1)

G1 (7)(7)(5)(5)(1)(1)
```



## Creating the Cyclometer Catalog Sudo Code

Settings that generated following double enciphered message keys

Machine WEHRMACHT early
Reflector Type UKW-A
Rotor Types III II I
Rotor Settings ABC
Ring Settings DEF
Plugboard Settings AB,CD,EF,GH,IJ,KL

```
LFMCWB	EPQIYU	CMDNAN	DDEVIV	JBGWEJ	GIYGJY	SGQPTU	ILCLDO	KQMRRB	CRINHL
CSJNOC	OLOEDS	XGXHTX	HDNMIE	APBKYA	DNOVBS	SCWPSR	DRJVHC	EFVIWT	LURCZG
XNKHBP	IBHLEI	SQWPRR	QFXQWX	QORQCG	BTPSUD	GDMGIB	TPDJYN	CWSNMQ	ZIXXJX
BXFSPM	PDLDIW	NWPUMD	VRWBHR	SYEPQV	UWROMG	UBXOEX	NKIULL	PDFDIM	VNDBBN
WPNYYE	DNHVBI	YAOFVS	GVCGKO	BEVSNT	SHOPGS	ZUXXZX	UBJOEC	LIQCJU	UYOOQS
EBPIED	VYHBQI	ZUGXZJ	ANJKBC	RAPZVD	MTDAUN	UNLOBW	KVIRKL	MSMAOB	WRGYHJ
NSOUOS	BJYSFY	IWJLMC	HTFMUM	XFJHWC	MCPASD	KDCRIO	RFXZWX	CAVNVT	YJDFFN
QQBQRA	MTMAUB	MSCAOO	GASGVQ	QAXQVX	QUBQZA	QGRQTG	QDOQIS	SEGPNJ	QKGQLJ
MPCAYO	PLRDDG	MDDAIN	HPAMYZ	AVXKKX	FYITQL	SQUPRH	SYSPQQ	KHLRGW	EFCIWO
LEQCNU	EGSITQ	MZWAXR	DHJVGC	PQWDRR	KKVRLT	QBYQEY	DASVVQ	JOFWCM	DCPVSD
```

For a double enciphered message key ABCDEF

Group 1 (G1) is A,D at position 1,4
Group 2 (G2) is B,E at position 2,5
Group 3 (G3) is C,F at position 3,6

Two Enigma Machines Enigma A and Enigma B are used to create the Cyclometer Catalog. 
Enigma B will be three steps ahead of Enigma A because the second character in each group is three positions ahead of the first character in that group.
