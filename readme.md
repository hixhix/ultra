# ULTRA

# Contents
1. [Installation](#installation)
2. [Start Menu](#start-menu)
3. [Interactive Enigma Menu](#interactive-enigma-menu)
4. [Enigma Cli Simulator Menu](#enigma-cli-simulator-menu)
5. [Code Sheets Menu](#code-sheets-menu)
6. [Cyclometer menu](#cyclometer-menu)
7. [Zygalski Sheets Menu](#zygalski-sheets-menu)
8. [Bombe Machine Menu](#bombe-machine-menu)
9. [Ring Setting Optomizer Menu](#ring-setting-optomizer-menu)
10. [Plugboard Optomizer Menu](#plugboard-optomizer-menu)
11. [Statistics Menu](#statistics-menu)
12. [Worked Examples](#worked-examples)


### Installation

```

```

### Start Menu
To see the start menu you can use python enigma_cli.py -h
```
positional arguments:
  {interactive_enigma,enigma_simulator,code_sheets,cyclometer,zygalski_sheets,bombe_machine,ring_optomizer,pb_optomizer,statistics}
    interactive_enigma  interactive enigma
    enigma_simulator    cli enigma
    code_sheets         code sheets
    cyclometer          cyclometer menu
    zygalski_sheets     zygalski sheets menu
    bombe_machine       bombe machine menu
    ring_optomizer      ring settings optomizer menu
    pb_optomizer        Plugboard optomizer menu
    statistics          statistics menu

optional arguments:
  -h, --help            show this help message and exit
```

### Interactive Enigma Menu
To see the interactive enigma menu run python enigma_cli.py interactive_enigma
```
Enter a number to select a machine.
1. WEHRMACHT early.
2. WEHRMACHT late.
3. LUFTWAFFE.
4. Kriegsmarine M3.
5. Kriegsmarine M4.
6. Quit.
```

### Enigma Cli Simulator Menu
To see the enigma simulator menu run python enigma_cli.py enigma_simulator -h
```
usage: enigma_cli.py enigma_simulator [-h] [-sc SCRAMBLER_CHARSET] [--scrambler-mode SCRAMBLER_MODE] [--rng-settings RNG_SETTINGS] [--rot-settings ROT_SETTINGS] [-pc PLUGBOARD_CHARSET]
                                      [--plugboard-mode PLUGBOARD_MODE] [--uhr-box-setting UHR_BOX_SETTING] [--plugboard-connections PLUGBOARD_CONNECTIONS] [-o OUTPUT_FILE]
                                      machine reflector rotors input-file

positional arguments:
  machine               Enigma machine type ( WEHRMACHT early | WEHRMACHT late | LUFTWAFFE | Kriegsmarine M3 | Kriegsmarine M4 )
  reflector             Reflector type in format "REF" 
                        WEHRMACHT early          ( UKW-A )
                        WEHRMACHT late           ( UKW-B | UKW-C )
                        LUFTWAFFE                ( UKW-B | UKW-C | UKW-D )
                        Kriegsmarine M3          ( UKW-B | UKW-C )
                        Kriegsmarine M4          ( UKW-B | UKW-C )
  rotors                Rotor types in format "R4,RS,RM,RF" or "RS,RM,RF" where
                        R4 = Static Rotor if applicable
                        RS = Slow Rotor
                        RM = Middle Rotor
                        RF = Fast Rotor
                         
                        WEHRMACHT early          (  )              [I, II, III]
                        WEHRMACHT late           (  )              [I, II, III, IV, V]
                        LUFTWAFFE                (  )              [I, II, III, IV, V, VI, VII, VIII]
                        Kriegsmarine M3          (  )              [I, II, III, IV, V, VI, VII, VIII]
                        Kriegsmarine M4          ( Beta | Gamma )  [I, II, III, IV, V, VI, VII, VIII]
  input-file            The input file path

optional arguments:
  -h, --help            show this help message and exit
  -sc SCRAMBLER_CHARSET, --scrambler-charset SCRAMBLER_CHARSET
                        Scrambler character set ( L | N ) where
                        L = Letters
                        N = Numbers
  --scrambler-mode SCRAMBLER_MODE
                        Scrambler turnover mode ( True | False )
  --rng-settings RNG_SETTINGS
                        Ring settings in format [RS,RM,RF]
  --rot-settings ROT_SETTINGS
                        Rotor settings in format [R4,RS,RM,RF] or [RS,RM,RF]
  -pc PLUGBOARD_CHARSET, --plugboard-charset PLUGBOARD_CHARSET
                        Plugboard character set ( L | N ) where
                        L = Letters
                        N = Numbers
  --plugboard-mode PLUGBOARD_MODE
                        Plugboard mode ( S | U ) where
                        S = Stecker
                        U = Uhr Box
  --uhr-box-setting UHR_BOX_SETTING
                        Uhr box setting in range 0 - 39
  --plugboard-connections PLUGBOARD_CONNECTIONS
                        Plugboard settings for stecker mode
                        in format [AB,CD,EF,GH,IJ,KL,M,N,O,P,QR,ST] letters mode
                        in format [1 2,3 4,5 6,7 8,9 10,11 12,13,14,15 16,17,18,19 20] numbers mode
                        Plugboard settings for uhr box mode
                        in format "A=[A,B,C,D,E,F,G,H,I,J] B=[K,L,M,N,O,P,Q,R,S,T]" letter mode
                        in format "A=[1,2,3,4,5,6,7,8,9,10] B=[11,12,13,14,15,16,17,18,19,20]" number mode
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        The output file path
```

### Code Sheets menu
To see the code sheets menu run python enigma_cli.py code_sheets -h
```
usage: enigma_cli.py code_sheets [-h] [-d] [-o OUTPUT_FILE] machine scrambler-char-flag plugboard-char-flag plugboard-mode

positional arguments:
  machine               Enigma machine type ( WEHRMACHT early | WEHRMACHT late | LUFTWAFFE | Kriegsmarine M3 | Kriegsmarine M4 )
  scrambler-char-flag   The scrambler charset flag 'L' or 'N'.
  plugboard-char-flag   The plugboard charset flag 'L' or 'N'.
  plugboard-mode        The plugboard mode 'S' or 'U'.

optional arguments:
  -h, --help            show this help message and exit
  -d, --dora-flag       Provide this flag with Luftwaffe enigma for rewireable UKW-D.
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
                        Optional output file. Will print to terminal if not provided.
```

### Cyclometer Menu
To see the cyclometer menu run python enigma_cli cyclometer -h
```
usage: enigma_cli.py cyclometer [-h] {generate_indicators,find_loops,filter_perms,catalog_menu} ...

positional arguments:
  {generate_indicators,find_loops,filter_perms,catalog_menu}
    generate_indicators
                        generate indicators
    find_loops          find loops
    filter_perms        filter permutations
    catalog_menu        catalog menu

optional arguments:
  -h, --help            show this help message and exit
```

### Zygalski Sheets Menu
To see the zygalski sheets menu run python enigma_cli.py zygalski_sheets -h
```
usage: enigma_cli.py zygalski_sheets [-h] {indicators,permutation_filter,group_indicators,ceaser_cipher_shift,zygalski_sheet,sheet_solution,zygalski_catalog} ...

positional arguments:
  {indicators,permutation_filter,group_indicators,ceaser_cipher_shift,zygalski_sheet,sheet_solution,zygalski_catalog}
    indicators          Generate and filter enigma indicators
    permutation_filter  Filters permutations
    group_indicators    Group indicators to isolate effects of middle rotor turnover
    ceaser_cipher_shift
                        Perform a ceaser cipher shift on a character string
    zygalski_sheet      Zygalski sheet menu
    sheet_solution      Creates a svg zygalski sheet solution on a lightboard
    zygalski_catalog    Create the wehrmacht zygalski sheets catalog

optional arguments:
  -h, --help            show this help message and exit
```

### Bombe Machine Menu
To see the bombe machine menu run python  enigma_cli.py bombe_machine -h
```
usage: enigma_cli.py bombe_machine [-h] {bombe_machine,filter_cribs} ...

positional arguments:
  {bombe_machine,filter_cribs}
    bombe_machine       Run the bombe machine
    filter_cribs        Filter cribs from cipher text using provided plain text

optional arguments:
  -h, --help            show this help message and exit
```

### Ring Setting Optomizer Menu
To see the ring optomizer menu run python enigma_cli.py ring_optomizer -h
```
usage: enigma_cli.py ring_optomizer [-h] permutation machine start_positions plugboard_settings cipher_text_file

positional arguments:
  permutation         the scrambler permutation
  machine             the enigma machine type
  start_positions     rotor start positions
  plugboard_settings  plugboard settings
  cipher_text_file    cipher text file path

optional arguments:
  -h, --help          show this help message and exit
```

### Plugboard Optomizer Menu
To see the plugboard optomizer menu run python enigma_cli.py pb_optomizer -h
```
usage: enigma_cli.py pb_optomizer [-h] text_file

positional arguments:
  text_file   The file path for the data file

optional arguments:
  -h, --help  show this help message and exit
```

### Statistics Menu
To see the statistics menu run python enigma_cli.py statistics -h
```
usage: enigma_cli.py statistics [-h] (-s INPUT_STRING | -i INPUT_FILE) (-b | -t | -ioc) [-o OUTPUT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  -s INPUT_STRING, --input-string INPUT_STRING
  -i INPUT_FILE, --input-file INPUT_FILE
  -b, --bigram
  -t, --trigram
  -ioc, --index_of_coincidence
  -o OUTPUT_FILE, --output-file OUTPUT_FILE
```

### Worked Examples

1. [Enigma Cli Worked Example](#enigma-cli-worked-example)
2. [Code Sheets Worked Example](#code-sheets-worked-example)
3. [Cyclometer Worked Example](#cyclometer-worked-example)
4. [Zygalski Sheets Worked Example](#zygalski-sheets-worked-example)
5. [Bombe Machine Worked Example](#bombe-machine-worked-example)
6. [Ring Setting Optomizer Worked Example](#ring-setting-optomizer-worked-example)
7. [Plugboard Optomizer Worked Example](#plugboard-optomizer-worked-example)
8. [Statistics Worked Example](#statistics-worked-example)


### Enigma Cli Simulator Worked Example
The enigma cli simulator can be used to create, configure and get output from an enigma machine. You need to
input the enigma machine type and then the reflector and rotor types to use. The plugboard has two mode, It can
operate as a standard stecker mode or it can operate using an uhr box. The character set for the scrambler and
plugboard will be either letters or numbers and can be configured seperatly.

#### Create an early Wehrmacht enigma machine
In this example we will create an early Wehrmacht enigma machine. We will configure this machine to use numbers
for its scrambler and letters for its plugboard. We will use the UKW-A reflector which is the only reflector type
available for the early Wehrmacht enigma and rotor types III for the slow rotor, II for the middle rotor and I
for the slow rotor. The plugboard mode we will use will be the standard stecker plugboard. The early Wehrmacht
enigma machine only used six plugboard cables. The number of plugboard cables is not enforced in the simulation
so we can use up to thirteen plugboard cables.

To see the options with the following command.
```
python enigma_cli.py enigma_simulator -h
```

```
python enigma_cli.py enigma_simulator "WEHRMACHT early" UKW-A "III,II,I" my_file.txt -sc N --rng-settings "01,02,03" --rot-settings "04,05,06" 
-pc L --plugboard-mode S --plugboard-connections "AB,CD,EF,GH,IJ,KL"
```

#### Create a Kriegsmarine M4 naval enigma
In this example we will create a Kriegsmarine M4 naval enigma machine. We will configure this machine to use letters
for its scrambler and numbers for its plugboard. We will use the UKW-B reflector which is one of two reflectors available
for this enigma machine, the other one being the UKW-C reflector. We will also use rotor types Beta for the fourth rotor,
IV for the slow rotor, V for the middle rotor and III for the fast rotor. We will use the standard stecker plugboard.

```
python enigma_cli.py enigma_simulator "Kriegsmarine M4" UKW-B "Beta,IV,V,III" test_message.txt -sc L --rng-settings "ABCD" --rot-settings "EFGH" 
-pc N --plugboard-mode S --plugboard-connections "01,02 03,04 05,06 07,08 09,10 11,12 13,14 15,16 17,18 19,20"
```

#### Create a Luftwaffe airforce enigma machine
In this example we will create a Luftwaffe airforce enigma machine. We will configure this machine to use numbers for 
its scrambler and letters for its plugboard. We will use the UKW-B reflector. We will also use rotor types III for the
slow rotor, II for the middle rotor and I for the fast rotor. We will use the uhr box with the plugboard. The uhr box was 
developed for the airforce but it is available with every enigma machine simulated here.

```
python enigma_cli.py enigma_simulator "Luftwaffe" UKW-B "III,II,I" test_message.txt -sc N --rng-settings "01,02,03" --rot-settings "04,05,06" -pc L --plugboard-mode U --plugboard-connections "A=[A,B,C,D,E,F,G,H,I,J] B=[K,L,M,N,O,P,Q,R,S,T]" --uhr-box-setting 31
```

### Code Sheets Worked Example

#### Create an early Wehrmacht enigma code sheet
To see the help menu for the code sheets menu run the following command.
```
python3 enigma_cli.py code_sheets -h
```

In this example we will create an early Wehrmacht enigma code sheet. We will use a numbers character set for the scrambler
and a letters character set for the plugboard. We will set the plugboard mode to the standard stecker plugboard mode.
```
python3 enigma_cli.py code_sheets "WEHRMACHT early" N L S
```

The following is an example of an early Wehrmacht enigma code sheet.
```
| DAY | UKW |   ROTOR TYPES    | RING SETTINGS | ROTOR SETTINGS | PLUGBOARD SETTINGS |
|     |     | RS    RM    RF   | RS   RM   RF  |  RS   RM   RF  |                    |
| 31  |  A  | III   II    I    | 07   01   10  |  06   18   15  | MG UN LY KB OZ IF  |
| 30  |  A  | I     III   II   | 05   10   26  |  15   18   07  | HC KB OP ZS AJ FI  |
| 29  |  A  | II    III   I    | 09   19   25  |  10   20   16  | UJ RA FC DX IB MZ  |
| 28  |  A  | I     III   II   | 02   09   20  |  11   21   17  | XZ CT DR PV YE LI  |
| 27  |  A  | III   I     II   | 16   13   21  |  21   17   02  | PQ SF DB RX EO LK  |
| 26  |  A  | II    I     III  | 02   09   14  |  09   07   14  | GJ EM HS WL DP TA  |
| 25  |  A  | I     III   II   | 08   07   13  |  22   13   11  | KC WQ BR DZ GF IA  |
| 24  |  A  | III   I     II   | 19   21   16  |  11   23   23  | DA TP FY QK ZJ CR  |
| 23  |  A  | II    III   I    | 12   12   17  |  17   06   25  | MP WU FS ZO GH TL  |
| 22  |  A  | I     III   II   | 25   22   02  |  19   12   18  | OS TM JK PG IR QX  |
| 21  |  A  | III   II    I    | 16   04   06  |  09   21   12  | NK MJ CO GS FD AH  |
| 20  |  A  | II    I     III  | 17   13   25  |  14   04   21  | TC WN LF YD GE ZB  |
| 19  |  A  | III   II    I    | 24   01   18  |  25   09   13  | AC XS PE TV MN UL  |
| 18  |  A  | II    I     III  | 25   11   15  |  25   09   01  | PY XG VF RO IL DT  |
| 17  |  A  | II    III   I    | 11   24   01  |  22   17   06  | KZ MU TP QH YX GJ  |
| 16  |  A  | I     II    III  | 14   11   24  |  22   25   02  | XF MC OT VE GQ RD  |
| 15  |  A  | I     II    III  | 03   01   02  |  25   04   08  | YF CD GK BU ST ZR  |
| 14  |  A  | I     II    III  | 02   23   08  |  04   10   12  | YX JN ZI RB CO TH  |
| 13  |  A  | I     II    III  | 02   25   11  |  14   06   14  | TV DK LI NC SF JY  |
| 12  |  A  | III   I     II   | 26   03   22  |  08   16   21  | BI FO WX LK RP EG  |
| 11  |  A  | I     III   II   | 17   22   14  |  24   02   18  | LN WU QI FZ AH CS  |
| 10  |  A  | III   II    I    | 26   09   14  |  11   04   26  | MB JL YW TA GD RH  |
| 09  |  A  | II    I     III  | 20   19   02  |  06   02   20  | SR OY BC PE MW NL  |
| 08  |  A  | III   II    I    | 05   09   25  |  16   11   15  | NS LV UF IJ OB ZD  |
| 07  |  A  | I     II    III  | 11   13   20  |  13   25   22  | SJ PT IF EC DX UY  |
| 06  |  A  | III   I     II   | 10   20   02  |  14   06   09  | SV IM XC AN GL RK  |
| 05  |  A  | III   II    I    | 14   05   20  |  18   13   06  | RQ CY VJ LP IB NK  |
| 04  |  A  | III   II    I    | 20   22   12  |  03   10   21  | KR YH PG BE IJ WZ  |
| 03  |  A  | III   I     II   | 23   19   10  |  22   26   09  | SC UJ GL ED WH FM  |
| 02  |  A  | III   I     II   | 26   07   23  |  23   19   07  | IU AS YX DF NC OR  |
| 01  |  A  | I     III   II   | 07   11   06  |  09   03   19  | MD GZ VR UL FB AJ  |
```

#### Create an Luftwaffe enigma code sheet
In this example we will make a Luftwaffe airforce code sheet that uses the rewireable UKW-D reflector. We will
use a numbers character set for the scrambler and a letters character set for the plugboard.
```
python enigma_cli.py code_sheets LUFTWAFFE N L S -d
```

```
| DAY |   ROTOR TYPES    | RING SETTINGS |  REF WIRE   |      PLUGBOARD SETTINGS       |    KENGRUPPEN     |
|     | RS    RM    RF   | RS   RM   RF  |             |                               |                   |
| 31  | VI    II    III  | 12   09   12  |             | NL VE ZM XS GH QK UY AI RW CP | 06/03/17 07/12/17 |
|     |                  |               |             |                               | 11/13/11 16/07/19 |
| 30  | VIII  I     VII  | 17   13   25  |             | CK FX TO WA DY SP NB JZ UG IL | 26/12/02 23/14/09 |
|     |                  |               |             |                               | 23/10/21 07/23/16 |
| 29  | II    VII   VI   | 04   13   08  |             | NE TQ SO MK LP ZR BF DG YW CI | 02/26/12 22/09/03 |
|     |                  |               |             |                               | 15/24/11 13/09/01 |
| 28  | V     I     VIII | 06   09   07  |             | UC BZ TY ND MH KI AO EP QS FR | 17/18/07 02/05/18 |
|     |                  |               | 04/24 11/23 |                               | 02/14/03 11/22/17 |
| 27  | II    IV    VI   | 02   23   26  | 01/13 10/26 | FK TM ES OD JQ YI PU BH RZ VC | 20/14/25 08/08/19 |
|     |                  |               | 08/18 03/25 |                               | 01/18/11 19/12/14 |
| 26  | IV    I     VI   | 25   26   09  | 14/17 06/21 | EX IU VY LZ PO FG QC DN JH TB | 16/22/05 21/08/09 |
|     |                  |               | 05/16 20/15 |                               | 19/01/23 20/23/25 |
| 25  | II    I     V    | 18   13   16  | 07/19 22/02 | OW VB TY DI RS JU KN AG PF XQ | 08/06/09 24/16/14 |
|     |                  |               |             |                               | 09/16/13 13/12/21 |
| 24  | II    I     VIII | 08   15   19  |             | CP FO KH NI YS AM DQ GZ RB TV | 26/02/19 23/09/17 |
|     |                  |               |             |                               | 10/08/12 09/24/07 |
| 23  | IV    VII   VI   | 16   04   03  |             | YV AW BK JG PT UQ XS HE CI NF | 17/13/04 22/26/11 |
|     |                  |               |             |                               | 24/16/13 08/06/12 |
| 22  | I     VI    III  | 20   04   16  |             | NT KW PL RQ CM OV ES ZG BI FD | 18/08/23 11/07/05 |
|     |                  |               |             |                               | 03/17/14 06/20/05 |
|-----|------------------|---------------|-------------|-------------------------------|-------------------|
| 21  | VII   II    III  | 06   13   19  |             | RG DV YE ZC FT SA ML HK PO WJ | 13/03/24 22/10/05 |
|     |                  |               |             |                               | 01/14/24 09/07/24 |
| 20  | V     VII   VIII | 16   12   07  |             | RN UX VW CI EY SL ZB FQ PO KG | 20/02/18 11/07/18 |
|     |                  |               |             |                               | 22/15/17 06/22/24 |
| 19  | III   V     VIII | 22   17   09  |             | UL KH FC JX IN RT SV YB AD GP | 16/05/26 13/07/07 |
|     |                  |               |             |                               | 12/01/02 13/16/08 |
| 18  | I     VII   VI   | 12   10   11  |             | RE YP XM GB JS IA DC TK WV QU | 23/22/14 10/15/12 |
|     |                  |               | 24/26 19/14 |                               | 04/20/23 07/16/03 |
| 17  | VII   V     II   | 09   25   07  | 17/02 22/21 | YW RF GZ BX AJ IK NU PQ TS ED | 09/08/20 13/15/17 |
|     |                  |               | 04/01 16/18 |                               | 05/11/15 17/16/07 |
| 16  | II    III   V    | 18   21   25  | 10/03 05/12 | BX IN YK AC GM ZJ EW SH VD UQ | 09/15/14 23/14/15 |
|     |                  |               | 13/07 23/20 |                               | 20/13/26 02/16/08 |
| 15  | VII   VIII  II   | 08   16   16  | 15/06 08/25 | GJ QY SO UA EV LM CB TP KZ HN | 04/17/10 04/14/13 |
|     |                  |               |             |                               | 04/06/18 10/24/18 |
| 14  | VI    I     VIII | 01   01   14  |             | HE VO SI FY TL QJ DN BW KA UC | 24/10/13 25/03/24 |
|     |                  |               |             |                               | 10/13/18 18/22/13 |
| 13  | IV    I     VIII | 13   21   07  |             | YM AE LP VU CH FO KX DI NQ RZ | 24/05/07 20/07/19 |
|     |                  |               |             |                               | 12/20/26 26/02/17 |
| 12  | I     III   VII  | 19   11   07  |             | JG RY BL AO QX EN VW DI TH FP | 22/11/01 21/03/15 |
|     |                  |               |             |                               | 20/15/03 14/19/17 |
|-----|------------------|---------------|-------------|-------------------------------|-------------------|
| 11  | I     II    VI   | 20   22   14  |             | SH ZU ED VX QJ MA BN KT GI YW | 01/06/22 01/06/11 |
|     |                  |               |             |                               | 18/11/19 26/11/24 |
| 10  | I     II    IV   | 23   08   11  |             | MF TR KW HI CS DN LV PZ JO XU | 24/07/01 21/16/02 |
|     |                  |               |             |                               | 25/26/10 16/18/21 |
| 09  | VII   VIII  I    | 13   16   02  |             | CN WH VX JD EL MO UQ ST ZR BK | 09/25/22 01/11/20 |
|     |                  |               |             |                               | 08/23/02 13/02/18 |
| 08  | V     VI    II   | 12   01   21  |             | CS XU EN DI ZM WH KJ YG OV TP | 24/11/05 06/18/09 |
|     |                  |               | 15/24 21/13 |                               | 20/12/17 21/01/04 |
| 07  | I     IV    VIII | 02   03   26  | 25/22 10/09 | TO KS UX CP NW GA VD FQ LZ MJ | 21/26/16 17/12/21 |
|     |                  |               | 18/16 05/02 |                               | 01/22/18 19/20/07 |
| 06  | I     II    VII  | 07   01   06  | 23/12 14/08 | EF GJ MZ KN TB LQ YW UC DS IA | 20/17/14 26/05/07 |
|     |                  |               | 17/26 03/11 |                               | 11/06/24 07/24/08 |
| 05  | II    IV    III  | 12   23   14  | 20/01 06/07 | HA XU OT WM KZ BF PJ VG QC DN | 08/21/01 21/06/09 |
|     |                  |               |             |                               | 12/11/22 21/07/10 |
| 04  | VIII  VI    V    | 17   24   16  |             | UJ SA YQ LD WI EN FR TV KP ZO | 24/13/10 19/20/06 |
|     |                  |               |             |                               | 16/22/02 10/23/07 |
| 03  | V     VI    VIII | 09   17   12  |             | QH MS OC DY XB NK AF LR TI VW | 11/25/02 17/24/10 |
|     |                  |               |             |                               | 17/07/18 14/09/22 |
| 02  | VI    I     II   | 25   13   25  |             | IW ZA KR UE FX MY CG SO LT HB | 06/06/13 06/09/05 |
|     |                  |               |             |                               | 14/21/23 08/26/14 |
| 01  | V     IV    III  | 09   06   03  |             | QA OD XR SG JE VP YF TK MN BZ | 21/02/22 18/25/09 |
|     |                  |               |             |                               | 15/19/18 15/03/26 |
```

#### Create an Kriegsmarine M4 enigma code sheet

```
python enigma_cli.py code_sheets "Kriegsmarine M4" L N S
```

```
| MSG ID | DAY | UKW |      ROTOR TYPES         | RING SETTINGS  | ROTOR SETTINGS |      PLUGBOARD SETTINGS       |
|        |     |     | R4    RS     RM     RF   | R4  RS  RM  RF | R4  RS  RM  RF |                               |
|  GMA   | 31  |  B  | Beta  II     VI     I    |  A   G   T   V |  E   U   S   V | 01/20 05/15 04/11 24/10 03/18 |
|        |     |     |                          |                |                | 13/07 25/23 09/22 19/06 08/16 |
|  KAL   | 30  |  C  | Beta  V      IV     II   |  A   Z   U   M |  R   E   Y   W | 12/26 02/10 16/08 24/25 17/18 |
|        |     |     |                          |                |                | 04/22 01/03 05/15 14/20 21/19 |
|  AAP   | 29  |  B  | Gamma VIII   VI     IV   |  A   L   U   C |  B   Q   D   E | 26/01 12/10 24/07 15/02 21/11 |
|        |     |     |                          |                |                | 23/14 06/03 13/08 22/05 04/19 |
|  UJL   | 28  |  C  | Gamma VII    V      II   |  A   K   A   W |  W   W   V   B | 13/09 22/06 19/05 17/24 18/20 |
|        |     |     |                          |                |                | 01/03 26/08 10/07 15/16 25/23 |
|  UTE   | 27  |  C  | Gamma VII    I      V    |  A   Z   H   E |  Q   K   H   F | 13/24 04/06 17/02 22/12 21/07 |
|        |     |     |                          |                |                | 14/23 03/16 15/09 11/25 20/01 |
|  XCK   | 26  |  B  | Gamma II     VII    III  |  A   O   X   S |  F   F   N   G | 20/12 18/05 01/11 06/02 25/13 |
|        |     |     |                          |                |                | 21/14 15/24 19/07 09/22 17/08 |
|  DJV   | 25  |  C  | Gamma II     V      VIII |  A   P   U   V |  L   Y   W   S | 05/03 17/14 16/04 25/13 19/21 |
|        |     |     |                          |                |                | 24/02 09/15 12/18 20/11 08/22 |
|  ZJP   | 24  |  C  | Beta  I      V      II   |  A   L   Q   B |  Z   W   A   P | 15/25 14/23 12/10 18/05 17/13 |
|        |     |     |                          |                |                | 24/26 04/22 16/20 06/07 01/03 |
|  HXL   | 23  |  C  | Gamma II     V      VI   |  A   N   L   Y |  D   E   M   F | 18/01 08/09 24/16 07/11 26/17 |
|        |     |     |                          |                |                | 25/05 02/21 20/15 10/04 19/14 |
|  JOP   | 22  |  B  | Gamma IV     V      II   |  A   R   M   W |  L   V   M   L | 24/10 06/25 07/21 03/01 19/13 |
|        |     |     |                          |                |                | 23/26 16/15 17/22 12/05 02/04 |
|  VBA   | 21  |  B  | Gamma V      III    IV   |  A   J   Q   M |  J   H   A   H | 19/26 25/20 11/13 17/16 21/07 |
|        |     |     |                          |                |                | 24/08 14/23 05/02 09/01 03/18 |
|  DVC   | 20  |  C  | Beta  III    II     IV   |  A   E   W   L |  R   S   E   G | 15/19 05/16 22/20 24/09 26/21 |
|        |     |     |                          |                |                | 08/23 18/11 12/02 03/17 10/04 |
|  STE   | 19  |  C  | Gamma VIII   VI     II   |  A   Q   O   I |  Y   S   T   U | 15/25 18/02 26/01 07/22 11/09 |
|        |     |     |                          |                |                | 05/23 24/20 19/13 21/14 08/17 |
|  HGM   | 18  |  C  | Beta  VII    II     VIII |  A   U   Q   T |  R   N   I   O | 21/07 09/17 24/23 26/02 15/04 |
|        |     |     |                          |                |                | 22/12 14/16 01/06 25/13 20/08 |
|  WVL   | 17  |  B  | Gamma VIII   III    VI   |  A   D   E   E |  H   X   K   Z | 14/18 17/20 03/08 23/16 04/15 |
|        |     |     |                          |                |                | 02/24 07/11 26/13 01/19 12/05 |
|  AFV   | 16  |  C  | Gamma VI     III    II   |  A   Q   J   P |  U   F   T   Z | 04/12 09/18 14/20 02/05 21/24 |
|        |     |     |                          |                |                | 01/11 17/16 19/15 06/25 10/13 |
|  FIN   | 15  |  B  | Beta  VIII   VI     III  |  A   G   X   P |  H   D   M   H | 01/20 21/06 03/26 22/05 15/25 |
|        |     |     |                          |                |                | 17/10 07/08 13/12 09/11 16/23 |
|  BIL   | 14  |  C  | Gamma VII    VI     II   |  A   S   V   C |  D   V   G   Y | 22/24 12/01 10/03 19/11 06/21 |
|        |     |     |                          |                |                | 25/14 09/08 26/13 18/17 05/07 |
|  PVK   | 13  |  C  | Beta  VI     VIII   III  |  A   P   P   R |  Y   O   D   K | 05/07 16/19 08/17 18/11 13/06 |
|        |     |     |                          |                |                | 10/25 22/02 01/03 12/23 09/15 |
|  RSB   | 12  |  B  | Gamma II     IV     VI   |  A   I   Q   C |  E   K   T   V | 15/04 02/14 16/09 25/17 11/24 |
|        |     |     |                          |                |                | 06/13 19/10 07/18 22/12 26/23 |
|  VNR   | 11  |  C  | Beta  VIII   I      VII  |  A   B   G   R |  A   X   P   K | 10/07 26/05 01/04 17/13 24/18 |
|        |     |     |                          |                |                | 25/02 16/21 11/20 06/12 08/23 |
|  VPI   | 10  |  B  | Beta  VIII   IV     I    |  A   F   P   G |  C   D   A   B | 25/11 07/23 01/16 12/03 04/21 |
|        |     |     |                          |                |                | 19/26 02/13 20/24 15/17 08/14 |
|  YKP   | 09  |  B  | Beta  II     V      VII  |  A   K   F   Q |  Q   E   L   U | 04/02 09/17 24/03 01/15 08/22 |
|        |     |     |                          |                |                | 18/12 26/13 21/05 11/07 16/19 |
|  FGP   | 08  |  B  | Beta  VIII   I      V    |  A   G   M   N |  V   F   X   D | 12/25 24/22 01/26 14/18 23/13 |
|        |     |     |                          |                |                | 09/02 20/06 07/15 10/16 04/03 |
|  RLV   | 07  |  B  | Beta  V      VIII   I    |  A   G   X   A |  R   V   K   I | 21/25 10/06 05/01 26/22 23/13 |
|        |     |     |                          |                |                | 08/15 24/17 09/12 19/07 18/14 |
|  QAB   | 06  |  C  | Gamma II     I      III  |  A   E   U   G |  D   L   J   Z | 07/18 21/02 16/11 14/17 26/06 |
|        |     |     |                          |                |                | 12/05 09/08 25/22 24/20 04/23 |
|  ATK   | 05  |  C  | Beta  VIII   IV     VII  |  A   R   V   Y |  Q   X   Y   H | 09/16 12/07 04/08 21/18 06/15 |
|        |     |     |                          |                |                | 23/24 10/02 17/19 20/25 05/03 |
|  JOE   | 04  |  B  | Gamma V      VIII   IV   |  A   B   O   Z |  R   Q   G   W | 23/08 10/09 03/06 14/02 11/07 |
|        |     |     |                          |                |                | 25/21 22/01 19/26 13/24 04/12 |
|  DZD   | 03  |  C  | Beta  V      VII    III  |  A   N   N   C |  U   M   F   S | 16/06 13/17 25/12 18/07 11/23 |
|        |     |     |                          |                |                | 19/20 24/05 21/04 22/14 26/08 |
|  BUQ   | 02  |  C  | Beta  V      I      IV   |  A   R   L   I |  M   W   Q   X | 21/18 24/08 12/05 04/06 26/03 |
|        |     |     |                          |                |                | 10/23 01/13 25/20 22/17 14/19 |
|  ETZ   | 01  |  C  | Gamma V      VI     IV   |  A   W   O   Q |  K   W   G   O | 01/16 08/15 19/14 25/10 17/26 |
|        |     |     |                          |                |                | 05/11 04/12 03/18 20/07 13/02 |

 AA = WA  BA = RC  CA = US  DA = MC  EA = BB  FA = JU  GA = KL  HA = CX  IA = GD  JA = PM  KA = TC  LA = NA  MA = QS 
  B = EW   B = EA   B = EV   B = HK   B = YM   B = WJ   B = AC   B = LM   B = UV   B = DN   B = FP   B = WH   B = BK 
  C = GB   C = ZV   C = MN   C = NU   C = LO   C = PR   C = ZX   C = YH   C = MG   C = TO   C = HI   C = FX   C = DA 
  D = LN   D = DS   D = XY   D = NX   D = WI   D = MS   D = IA   D = TS   D = UG   D = DT   D = MJ   D = KT   D = PD 
  E = HR   E = KX   E = VN   E = WO   E = WK   E = XO   E = DI   E = ZT   E = QB   E = CT   E = NZ   E = JM   E = JI 
  F = RL   F = HZ   F = NO   F = UE   F = PU   F = XV   F = CO   F = GY   F = TJ   F = UO   F = OR   F = JK   F = FZ 
  G = TT   G = HY   G = QK   G = ZO   G = RR   G = SI   G = RN   G = UA   G = QN   G = AU   G = WX   G = AV   G = IC 
  H = PF   H = SV   H = IL   H = LU   H = WS   H = TR   H = XD   H = GP   H = EZ   H = RP   H = JW   H = EI   H = NQ 
  I = XL   I = XR   I = IO   I = GE   I = LH   I = NM   I = IV   I = KC   I = VA   I = ME   I = OE   I = SH   I = ZB 
  J = HJ   J = TL   J = GZ   J = XM   J = PE   J = TZ   J = YY   J = AJ   J = WY   J = VP   J = MV   J = IT   J = KD 
  K = VC   K = MB   K = DQ   K = NC   K = SS   K = MR   K = UR   K = DB   K = DX   K = LF   K = ES   K = OY   K = SJ 
  L = HM   L = NT   L = RZ   L = GL   L = KM   L = UF   L = DL   L = YE   L = CH   L = TH   L = GA   L = ZH   L = UQ 
  M = SN   M = TQ   M = AS   M = SO   M = TE   M = PN   M = HO   M = AL   M = DR   M = LE   M = EL   M = HB   M = WM 
  N = NY   N = NS   N = XJ   N = JB   N = WB   N = XI   N = BZ   N = OL   N = RG   N = YL   N = WW   N = AD   N = CC 
  O = QO   O = SC   O = GF   O = OI   O = KS   O = YA   O = NV   O = GM   O = CI   O = PL   O = YX   O = EC   O = UB 
  P = PI   P = GS   P = SU   P = LV   P = QZ   P = KB   P = HH   P = GV   P = HQ   P = QH   P = XB   P = BX   P = AR 
  Q = PG   Q = PY   Q = KZ   Q = CK   Q = NF   Q = TV   Q = OM   Q = IP   Q = UX   Q = LS   Q = TM   Q = FW   Q = WG 
  R = MP   R = OV   R = OB   R = IM   R = HT   R = WE   R = BU   R = AE   R = XZ   R = CW   R = PT   R = WP   R = FK 
  S = CM   S = WL   S = UW   S = BD   S = KK   S = PJ   S = BP   S = ZD   S = RK   S = WF   S = EO   S = JQ   S = FD 
  T = TG   T = TF   T = JE   T = JD   T = OZ   T = OH   T = VI   T = ER   T = LJ   T = ZF   T = LD   T = XA   T = NE 
  U = JG   U = GR   U = EU   U = YJ   U = CU   U = OC   U = YI   U = WT   U = NR   U = FA   U = YW   U = DH   U = JZ 
  V = LG   V = HX   V = XT   V = JY   V = CB   V = OW   V = HP   V = WC   V = GI   V = OU   V = YS   V = DP   V = KJ 
  W = UU   W = QU   W = JR   W = IX   W = AB   W = LQ   W = XW   W = NN   W = ZA   W = KH   W = SQ   W = VL   W = NG 
  X = WV   X = LP   X = HA   X = IK   X = RX   X = LC   X = NB   X = BV   X = DW   X = PX   X = BE   X = WZ   X = RE 
  Y = YT   Y = XF   Y = OS   Y = VJ   Y = ON   Y = VK   Y = HF   Y = BG   Y = PV   Y = DV   Y = TN   Y = ZL   Y = UZ 
  Z = RJ   Z = GN   Z = XQ   Z = ZK   Z = IH   Z = MF   Z = CJ   Z = BF   Z = QA   Z = MU   Z = CQ   Z = SA   Z = SW 

 NA = LA  OA = UL  PA = YG  QA = IZ  RA = PH  SA = LZ  TA = OP  UA = HG  VA = II  WA = AA  XA = LT  YA = FO  ZA = IW 
  B = GX   B = CR   B = XK   B = IE   B = VR   B = VY   B = ZW   B = MO   B = ZP   B = EN   B = KP   B = UK   B = MI 
  C = DK   C = FU   C = ZY   C = OG   C = BA   C = BO   C = KA   C = VF   C = AK   C = HV   C = TW   C = WR   C = PS 
  D = XG   D = UY   D = MD   D = UN   D = UH   D = VV   D = QF   D = YU   D = SZ   D = UP   D = GH   D = SX   D = HS 
  E = MT   E = KI   E = EJ   E = VO   E = MX   E = UJ   E = EM   E = DF   E = RY   E = FR   E = RQ   E = HL   E = QP 
  F = EQ   F = RV   F = AH   F = TD   F = ZS   F = QX   F = BT   F = FL   F = UC   F = JS   F = BY   F = SK   F = JT 
  G = MW   G = QC   G = AQ   G = PW   G = IN   G = RW   G = AT   G = ID   G = NP   G = MQ   G = ND   G = PA   G = QW 
  H = SR   H = FT   H = RA   H = JP   H = TX   H = LI   H = JL   H = RD   H = YR   H = LB   H = ZZ   H = HC   H = LL 
  I = YN   I = DO   I = AP   I = RI   I = QI   I = FG   I = OT   I = XP   I = GT   I = ED   I = FN   I = GU   I = OK 
  J = QQ   J = XX   J = FS   J = YZ   J = AZ   J = MK   J = IF   J = SE   J = DY   J = FB   J = CN   J = DU   J = VT 
  K = ZR   K = ZI   K = SP   K = CG   K = IS   K = YF   K = RM   K = YB   K = FY   K = EE   K = PB   K = TP   K = DZ 
  L = RU   L = HN   L = JO   L = YQ   L = AF   L = VX   L = BJ   L = OA   L = LW   L = BS   L = AI   L = JN   L = LY 
  M = FI   M = GQ   M = JA   M = OO   M = TK   M = RT   M = KQ   M = YO   M = WU   M = MM   M = DJ   M = EB   M = VQ 
  N = HW   N = EY   N = FM   N = IG   N = GG   N = AM   N = KY   N = QD   N = CE   N = OQ   N = WQ   N = NI   N = VU 
  O = CF   O = QM   O = ZU   O = AO   O = TU   O = DM   O = JC   O = JF   O = QE   O = DE   O = FE   O = UM   O = DG 
  P = VG   P = TA   P = OX   P = ZE   P = JH   P = PK   P = YK   P = WD   P = JJ   P = LR   P = UI   P = UT   P = VB 
  Q = MH   Q = WN   Q = QY   Q = NJ   Q = XE   Q = KW   Q = BM   Q = ML   Q = ZM   Q = XN   Q = CZ   Q = QL   Q = PZ 
  R = IU   R = KF   R = FC   R = YV   R = EG   R = NH   R = FH   R = GK   R = RB   R = YC   R = BI   R = VH   R = NK 
  S = BN   S = CY   S = ZC   S = MA   S = ST   S = EK   S = HD   S = CA   S = QV   S = EH   S = VZ   S = KV   S = RF 
  T = BL   T = TI   T = KR   T = NW   T = SM   T = RS   T = AG   T = YP   T = ZJ   T = HU   T = CV   T = AY   T = HE 
  U = DC   U = JV   U = EF   U = BW   U = NL   U = CP   U = RO   U = AW   U = ZN   U = VM   U = SY   U = UD   U = PO 
  V = GO   V = BR   V = IY   V = VS   V = OF   V = BH   V = FQ   V = IB   V = SD   V = AX   V = FF   V = QR   V = BC 
  W = QT   W = FV   W = QG   W = ZG   W = SG   W = MZ   W = XC   W = CS   W = TY   W = KN   W = GW   W = KU   W = TB 
  X = DD   X = PP   X = JX   X = SF   X = EX   X = YD   X = RH   X = IQ   X = SL   X = KG   X = OJ   X = KO   X = GC 
  Y = AN   Y = LK   Y = BQ   Y = PQ   Y = VE   Y = XU   Y = VW   Y = OD   Y = SB   Y = IJ   Y = CD   Y = GJ   Y = PC 
  Z = KE   Z = ET   Z = ZQ   Z = EP   Z = CL   Z = VD   Z = FJ   Z = MY   Z = XS   Z = LX   Z = IR   Z = QJ   Z = XH 
```

### Cyclometer Worked Example

```
python enigma_cli.py cyclometer generate_indicators "WEHRMACHT early" UKW-A "III,II,I" "ABC" "DEF" "AB,CD,EF,GH,IJ,KL" 200 > indicators.txt
```

```
python enigma_cli.py cyclometer find_loops indicators.txt
```

```
G1 (7)(7)(5)(5)(1)(1) G2 (10)(10)(3)(3) G3 (12)(12)(1)(1)
```

```
python enigma_cli.py cyclometer filter_perms "WEHRMACHT early" "G1 (7)(7)(5)(5)(1)(1) G2 (10)(10)(3)(3) G3 (12)(12)(1)(1)"
```

```
UKW-A_I_II_III     OGC
UKW-A_I_III_II     OBV
UKW-A_I_III_II     WGW
UKW-A_I_III_II     XJI
UKW-A_II_I_III     JDU
UKW-A_II_I_III     UOZ
UKW-A_II_III_I     DNC
UKW-A_II_III_I     HDT
UKW-A_II_III_I     LIY
UKW-A_II_III_I     XYL
UKW-A_III_I_II     GNH
UKW-A_III_I_II     RTT
UKW-A_III_II_I     GCV
UKW-A_III_II_I     VMD
UKW-A_III_II_I     XPE
UKW-A_III_II_I     XXX
```

### Zygalski Sheets Worked Example


### Bombe Machine Worked Example


### Herivel Square Example


### Ring Setting optomizer Worked Example


### Plugboard Optomizer Worked Example


### Statistics Worked Example

