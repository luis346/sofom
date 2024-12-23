// datos.js
const QUINCENAS = [
    ['4', '4 QUINCENA(S)'],
    ['6', '6 QUINCENA(S)'],
    ['8', '8 QUINCENA(S)'],
    ['10', '10 QUINCENA(S)'],
    ['12', '12 QUINCENA(S)'],
    ['14', '14 QUINCENA(S)'],
    ['16', '16 QUINCENA(S)'],
    ['18', '18 QUINCENA(S)'],
    ['20', '20 QUINCENA(S)'],
    ['24', '24 QUINCENA(S)'],
    ['26', '26 QUINCENA(S)'],
    ['28', '28 QUINCENA(S)'],
    ['30', '30 QUINCENA(S)'],
    ['34', '34 QUINCENA(S)'],
    ['36', '36 QUINCENA(S)'],
    ['38', '38 QUINCENA(S)'],
    ['40', '40 QUINCENA(S)'],
    ['42', '42 QUINCENA(S)'],
    ['44', '44 QUINCENA(S)'],
    ['46', '46 QUINCENA(S)'],
    ['48', '48 QUINCENA(S)'],
    ['50', '50 QUINCENA(S)'],
    ['52', '52 QUINCENA(S)'],
    ['54', '54 QUINCENA(S)'],
    ['56', '56 QUINCENA(S)'],
    ['58', '58 QUINCENA(S)'],
    ['60', '60 QUINCENA(S)'],
    ['62', '62 QUINCENA(S)'],
    ['64', '64 QUINCENA(S)'],
    ['66', '66 QUINCENA(S)'],
    ['68', '68 QUINCENA(S)'],
    ['70', '70 QUINCENA(S)'],
    ['72', '72 QUINCENA(S)'],
    ['74', '74 QUINCENA(S)'],
    ['76', '76 QUINCENA(S)'],
    ['78', '78 QUINCENA(S)'],
    ['80', '80 QUINCENA(S)'],
    ['82', '82 QUINCENA(S)'],
    ['84', '84 QUINCENA(S)'],
    ['86', '86 QUINCENA(S)'],
    ['88', '88 QUINCENA(S)'],
    ['90', '90 QUINCENA(S)'],
    ['92', '92 QUINCENA(S)'],
    ['94', '94 QUINCENA(S)'],
    ['96', '96 QUINCENA(S)'],
    ['98', '98 QUINCENA(S)'],
    ['100', '100 QUINCENA(S)'],
    ['102', '102 QUINCENA(S)'],
    ['104', '104 QUINCENA(S)'],
    ['106', '106 QUINCENA(S)'],
    ['108', '108 QUINCENA(S)'],
    ['112', '112 QUINCENA(S)'],
    ['114', '114 QUINCENA(S)'],
    ['116', '116 QUINCENA(S)'],
    ['118', '118 QUINCENA(S)'],
    ['120', '120 QUINCENA(S)'],
    ['124', '124 QUINCENA(S)'],
    ['126', '126 QUINCENA(S)'],
    ['128', '128 QUINCENA(S)'],
    ['130', '130 QUINCENA(S)'],
    ['134', '134 QUINCENA(S)'],
    ['136', '136 QUINCENA(S)'],
    ['138', '138 QUINCENA(S)'],
    ['140', '140 QUINCENA(S)'],
    ['142', '142 QUINCENA(S)'],
    ['144', '144 QUINCENA(S)'],
    ['146', '146 QUINCENA(S)'],
    ['148', '148 QUINCENA(S)'],
    ['150', '150 QUINCENA(S)']
];

const MESES = [
    ['1', '1 MESES'],
    ['2', '2 MESES'],
    ['3', '3 MESES'],
    ['4', '4 MESES'],
    ['5', '5 MESES'],
    ['6', '6 MESES'],
    ['7', '7 MESES'],
    ['8', '8 MESES'],
    ['9', '9 MESES'],
    ['10', '10 MESES'],
    ['11', '11 MESES'],
    ['12', '12 MESES'],
    ['13', '13 MESES'],
    ['14', '14 MESES'],
    ['15', '15 MESES'],
    ['16', '16 MESES'],
    ['17', '17 MESES'],
    ['18', '18 MESES'],
    ['19', '19 MESES'],
    ['20', '20 MESES'],
    ['21', '21 MESES'],
    ['22', '22 MESES'],
    ['23', '23 MESES'],
    ['24', '24 MESES'],
    ['25', '25 MESES'],
    ['26', '26 MESES'],
    ['27', '27 MESES'],
    ['28', '28 MESES'],
    ['29', '29 MESES'],
    ['30', '30 MESES'],
    ['31', '31 MESES'],
    ['32', '32 MESES'],
    ['33', '33 MESES'],
    ['34', '34 MESES'],
    ['35', '35 MESES'],
    ['36', '36 MESES'],
    ['37', '37 MESES'],
    ['38', '38 MESES'],
    ['39', '39 MESES'],
    ['40', '40 MESES'],
    ['41', '41 MESES'],
    ['42', '42 MESES'],
    ['43', '43 MESES'],
    ['44', '44 MESES'],
    ['45', '45 MESES'],
    ['46', '46 MESES'],
    ['47', '47 MESES'],
    ['48', '48 MESES'],
    ['49', '49 MESES'],
    ['50', '50 MESES'],
    ['51', '51 MESES'],
    ['52', '52 MESES'],
    ['53', '53 MESES'],
    ['54', '54 MESES'],
    ['55', '55 MESES'],
    ['56', '56 MESES'],
    ['57', '57 MESES'],
    ['58', '58 MESES'],
    ['59', '59 MESES'],
    ['60', '60 MESES'],
    ['61', '61 MESES'],
    ['62', '62 MESES'],
    ['63', '63 MESES'],
    ['64', '64 MESES'],
    ['65', '65 MESES'],
    ['66', '66 MESES'],
    ['67', '67 MESES'],
    ['68', '68 MESES'],
    ['69', '69 MESES'],
    ['70', '70 MESES'],
    ['71', '71 MESES'],
    ['72', '72 MESES'],
    ['73', '73 MESES'],
    ['74', '74 MESES'],
    ['75', '75 MESES'],
    ['76', '76 MESES'],
    ['77', '77 MESES'],
    ['78', '78 MESES'],
    ['79', '79 MESES'],
    ['80', '80 MESES'],
    ['81', '81 MESES'],
    ['82', '82 MESES'],
    ['83', '83 MESES'],
    ['84', '84 MESES'],
    ['85', '85 MESES'],
    ['86', '86 MESES'],
    ['87', '87 MESES'],
    ['88', '88 MESES'],
    ['89', '89 MESES'],
    ['90', '90 MESES'],
];

