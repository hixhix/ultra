# Cyclometer Catalog

Settings that generated following double enciphered message keys

Machine WEHRMACHT early
Reflector Type UKW-A
Rotor Types III II I
Rotor Settings ABC
Ring Settings DEF
Plugboard Settings AB,CD,EF,GH,IJ,KL

```
WYAYQZ	BLPSDD	GBQGEU	ARRKHG	CSXNOX	JKOWLS	OFWEWR	BMKSAP	JFCWWO	WLOYDS
WUHYZI	UCROSG	KODRCN	XYFHQM	VOKBCP	IWULMH	BACSVO	BANSVE	FSETOV	PGRDTG
KGERTV	KLSRDQ	SMUPAH	OHPEGD	FDOTIS	VZRBXG	AIAKJZ	WPXYYX	ZIHXJI	CABNVA
VPSBYQ	UXIOPL	NGRUTG	VAIBVL	DDLVIW	OWEEMV	AKOKLS	IMBLAA	UZDOXN	LOBCCA
AESKNQ	TMVJAT	EOLICW	ZUDXZN	EIZIJK	VEABNZ	FCNTSE	ROHZCI	OSLEOW	UJTOFF
SZAPXZ	PLBDDA	XGLHTW	ICILSL	LLCCDO	DNJVBC	GOWGCR	JOPWCD	SPVPYT	UPQOYU
TIZJJK	TPOJYS	BXCSPO	CFGNWJ	JWDWMN	PQKDRP	MRXAHX	VICBJO	NCRUSG	NVMUKB
KFKRWP	BYQSQU	CTONUS	QSPQOD	JVRWKG	MSQAOU	EBUIEH	EAHIVI	IIALJZ	TATJVF
YGFFTM	MDAAIZ	HOLMCW	WXTYPF	YCLFSW	JOIWCL	LANCVE	JNPWBD	HWWMMR	IVNLKE
HAGMVJ	BGDSTN	REIZNL	MPCAYO	EMPIAD	YKUFLH	CJSNFQ	OMNEAE	VJABFZ	EKZILK
VIVBJT	JSDWON	WDKYIP	NLMUDB	OKBELA	ZJYXFY	RGIZTL	KEMRNB	YIXFJX	FSMTOB
KJVRFT	MCGASJ	HCZMSK	VDOBIS	RZNZXE	CDANIZ	XDVHIT	NTYUUY	UMQOAU	HDZMIK
DPRVYG	PMPDAD	XAWHVR	SFSPWQ	JEOWNS	ERGIHJ	TZAJXZ	UKHOLI	KTKRUP	QUXQZX
OYJEQC	OZMEXB	MHSAGQ	YZRFXG	TBFJEM	SOWPCR	QTYQUY	FPSTYQ	KOJRCC	TYUJQH
MQFARM	FPFTYM	BDOSIS	MVPAKD	RXNZPE	XDDHIN	OUAEZZ	KBSREQ	WRZYHK	SIHPJI
```

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

AESKNQ
KGERTV
REIZNL
ZUDXZN
XGLHTW
HAGMVJ
MQFARM

AKRZXHM

CYCLE 2

ABCDEFGHIJKLMNOPQRSTUVWXYZ
-      -  - -    -     - -

BLPSDD
SZAPXZ
PLBDDA
DPRVYG
VAIBVL

BSPDV

CYCLE 3

ABCDEFGHIJKLMNOPQRSTUVWXYZ
-- -   -  - -  - --  - - -

CTONUS
NGRUTG
UCROSG
OYJEQC
EOLICW
ICILSL
LANCVE

CNUOEIL

CYCLE 4

ABCDEFGHIJKLMNOPQRSTUVWXYZ
-----  -- ------ -- -- - -

FPFTYM
TIZJJK
JSDWON
WYAYQZ
YGFFTM

FTJWY

CYCLE 5

ABCDEFGHIJKLMNOPQRSTUVWXYZ
------ --------- ---------

GBQGEU

G

CYCLE 6

ABCDEFGHIJKLMNOPQRSTUVWXYZ
---------------- ---------

QSPQOD

Q

CYCLE 7

ABCDEFGHIJKLMNOPQRSTUVWXYZ
--------------------------

The cycles of letters for Group 1 G1 are as follows.

G1 (AKRZXHM)(BSPDV)(CNUOEIL)(FTJWY)(G)(Q)

Convert the cycle strings to the number of letters in each cycle.

G1 (7)(5)(7)(5)(1)(1)

Order the cycle lengths in descending order.

G1 (7)(7)(5)(5)(1)(1)

Using the method above to solve for all three Cycle Groups G1,G2 and G3.

G1 (7)(7)(5)(5)(1)(1) G2 (10)(10)(3)(3) G3 (12)(12)(1)(1)
```



## Creating the Cyclometer Catalog Sudo Code

A Cyclometer Catalog will be created for each Reflector Type and Rotor Wheel Order.
In each Cyclometer Catalog there will be an entry for each Rotor Ground Setting in the range 'AAA' to 'ZZZ' and the three Cycle Groups G1,G2,G3.

The Enigma Machine will have its Reflector Type and Rotor Wheel Order set.
There will be no plugboard settings as the letter swapping performed by the plugboard does not effect numbers in the Cycle Groups.
For each Rotor Ground Setting every possible Message Key in the range 'AAA' to 'ZZZ' will be input twice to produce a Double Enciphered Message Key.
After each Message Key is input the Enigma Machine will be reset to the same Rotor Ground Setting.
The turnover functionality of the Enigma Machine should be disabled such that only the Fast Rotor can turnover.
This is to ensure that the Cyclometer Catalog will not be influenced by the effect of the Middle Rotor turning over.
The length of the Double Enciphered Message Key is only six letters and so it is unlikely that the Middle Rotor would have turned over when the message key was typed in to the Enigma Machine.
When all of the Double Enciphered Message Keys have been generated for all possible Message Keys in the range 'AAA' to 'ZZZ' the cycles will be solved for G1,G2 and G3 using the same method shown above.
Below is an example of some entries in a Cyclometer Catalog.

```
AAA G1 (6)(6)(5)(5)(2)(2)	G2 (13)(13)		G3 (11)(11)(2)(2)
AAB G1 (13)(13)			G2 (11)(11)(2)(2)	G3 (5)(5)(4)(4)(4)(4)
AAC G1 (11)(11)(2)(2)		G2 (5)(5)(4)(4)(4)(4)	G3 (5)(5)(4)(4)(4)(4)
```
