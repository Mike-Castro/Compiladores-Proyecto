
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ASSIGN BOOL COMMA CTEF CTEI CTESTRING DIVIDE DO ELSE END EQ FLOAT FOR FUNC GT GTE ID IF INT LBRACE LBRACKET LPAREN LT LTE MAIN MINUS MOD NEQ NOT OR PLUS PROGRAM RBRACE RBRACKET READ RETURN RPAREN SEMICOLON STRING TIMES VOID WHILE WRITEprogram : PROGRAM ID SEMICOLON declaration_list function MAIN LPAREN mainRef RPAREN bloque SEMICOLON final debug dataObjmainRef :\n    final : \n    debug : \n    dataObj : \n    tipo : INT\n            | FLOAT\n            | STRINGbloque : LBRACE bloqueB RBRACEbloqueB : statement_list bloqueB\n                | emptyfunction : functionF function\n                | emptyfunctionF : FUNC idFunc LPAREN parameter_list RPAREN LBRACE statement_list RBRACE SEMICOLON terminaFunc\n    idFunc : ID\n    callFunc : ID LPAREN parameter_list RPAREN SEMICOLONterminaFunc :\n    parameter_list : tipo ID parameter\n                      | emptyparameter : COMMA tipo ID parameter\n                 | emptystatement_list : statement\n                      | statement_list statementstatement : declaration_list\n                 | assignment_statement\n                 | read_statement\n                 | write_statement\n                 | if_statement\n                 | for_statement\n                 | while_statement\n                 | do_while_statement\n                 | return_statement\n                 | callFuncexpression : exp1\n                    | exp1 AND exp1\n                    | exp1 OR exp1exp1 : exp\n            | exp LT exp\n            | exp GT exp\n            | exp EQ exp\n            | exp NEQ expexp : term \n             | term PLUS exp\n             | term MINUS expterm : fact\n         | fact TIMES term\n         | fact DIVIDE termfact : ID addOp\n            | CTEF addConst\n            | CTEI addConst\n            | CTESTRING addConst\n            | LPAREN expression RPARENaddOp : \n    addConst : \n    declaration_list : declaration\n                        | declaration_list declarationdeclaration : tipo ID SEMICOLON\n                    | tipo ID COMMA declarationDdeclarationD : ID COMMA declarationD\n                    | ID SEMICOLONlist_declaration : tipo ID LBRACKET var RBRACKET SEMICOLONvar : CTEImatrix_declaration : tipo ID LBRACKET var RBRACKET LBRACKET var RBRACKET SEMICOLONassignment_statement : ID ASSIGN exp SEMICOLON\n                            | list_declaration\n                            | matrix_declarationread_statement : READ LPAREN ID RPAREN SEMICOLONwrite_statement : WRITE LPAREN write_list RPAREN SEMICOLONwrite_list : write_item\n                       | write_list COMMA write_itemwrite_item : factif_statement : IF LPAREN expression if2 RPAREN LBRACE statement_list RBRACE condif if3condif : ELSE if4 LBRACE statement_list RBRACE SEMICOLON \n              | SEMICOLONif2 : \n    if3 : \n    if4 : \n    while_statement : WHILE LPAREN while1 expression while2 RPAREN LBRACE statement_list RBRACE while3 SEMICOLONwhile1 : \n    while2 : \n    while3 : \n    do_while_statement : DO dowhile1 LBRACE statement_list RBRACE WHILE LPAREN expression dowhile2 RPAREN SEMICOLONdowhile1 : \n    dowhile2 : \n    for_statement : FOR LPAREN assignment_statement SEMICOLON expression SEMICOLON assignment_statement RPAREN LBRACE statement_list RBRACEreturn_statement : RETURN expression SEMICOLONempty : '
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,43,71,97,129,],[0,-3,-4,-5,-1,]),'ID':([2,6,7,8,9,10,12,15,21,22,26,29,31,32,36,38,39,45,47,48,49,50,51,52,53,54,55,56,57,59,60,67,68,69,70,74,75,77,78,79,80,81,92,95,107,108,109,110,111,112,113,114,115,116,117,118,119,120,130,134,136,139,154,155,156,163,164,168,169,171,172,176,179,181,182,185,186,188,191,192,193,194,195,197,],[3,-55,16,-6,-7,-8,-56,20,-57,25,-58,35,25,-60,-59,58,58,58,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,88,93,58,96,-22,88,100,88,88,106,-79,88,-23,137,88,58,-86,88,88,88,88,88,88,88,88,88,88,-64,88,88,58,-16,-67,-68,58,106,-61,58,58,88,58,-76,-74,58,-63,-72,58,58,-85,-78,-82,58,-73,]),'SEMICOLON':([3,16,25,37,59,60,72,83,84,85,86,87,88,89,90,91,93,94,98,105,121,122,123,124,130,131,132,133,140,141,142,143,144,145,146,147,148,149,150,159,162,168,174,178,183,185,189,190,196,],[4,21,32,43,-65,-66,-9,110,-34,-37,-42,-45,-53,-54,-54,-54,21,127,130,136,-48,-49,-50,-51,-64,154,155,156,-35,-36,-38,-39,-40,-41,-43,-44,-46,-47,-52,164,168,-61,181,185,-81,-63,193,194,197,]),'INT':([4,5,6,12,21,24,26,32,36,38,39,41,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,76,80,95,109,110,130,139,154,155,156,163,164,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[8,8,-55,-56,-57,8,-58,-60,-59,8,8,8,8,-22,8,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,8,-22,8,8,-23,8,-86,-64,8,-16,-67,-68,8,8,-61,8,8,8,-76,-74,8,-63,-72,8,8,-85,-78,-82,8,-73,]),'FLOAT':([4,5,6,12,21,24,26,32,36,38,39,41,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,76,80,95,109,110,130,139,154,155,156,163,164,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[9,9,-55,-56,-57,9,-58,-60,-59,9,9,9,9,-22,9,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,9,-22,9,9,-23,9,-86,-64,9,-16,-67,-68,9,9,-61,9,9,9,-76,-74,9,-63,-72,9,9,-85,-78,-82,9,-73,]),'STRING':([4,5,6,12,21,24,26,32,36,38,39,41,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,76,80,95,109,110,130,139,154,155,156,163,164,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[10,10,-55,-56,-57,10,-58,-60,-59,10,10,10,10,-22,10,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,10,-22,10,10,-23,10,-86,-64,10,-16,-67,-68,10,10,-61,10,10,10,-76,-74,10,-63,-72,10,10,-85,-78,-82,10,-73,]),'FUNC':([5,6,12,13,21,26,32,36,127,153,],[15,-55,-56,15,-57,-58,-60,-59,-17,-14,]),'MAIN':([5,6,11,12,13,14,18,21,26,32,36,127,153,],[-87,-55,17,-56,-87,-13,-12,-57,-58,-60,-59,-17,-14,]),'READ':([6,12,21,26,32,36,38,39,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,95,109,110,130,139,154,155,156,163,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[-55,-56,-57,-58,-60,-59,61,61,61,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,61,-22,-23,61,-86,-64,61,-16,-67,-68,61,-61,61,61,61,-76,-74,61,-63,-72,61,61,-85,-78,-82,61,-73,]),'WRITE':([6,12,21,26,32,36,38,39,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,95,109,110,130,139,154,155,156,163,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[-55,-56,-57,-58,-60,-59,62,62,62,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,62,-22,-23,62,-86,-64,62,-16,-67,-68,62,-61,62,62,62,-76,-74,62,-63,-72,62,62,-85,-78,-82,62,-73,]),'IF':([6,12,21,26,32,36,38,39,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,95,109,110,130,139,154,155,156,163,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[-55,-56,-57,-58,-60,-59,63,63,63,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,63,-22,-23,63,-86,-64,63,-16,-67,-68,63,-61,63,63,63,-76,-74,63,-63,-72,63,63,-85,-78,-82,63,-73,]),'FOR':([6,12,21,26,32,36,38,39,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,95,109,110,130,139,154,155,156,163,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[-55,-56,-57,-58,-60,-59,64,64,64,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,64,-22,-23,64,-86,-64,64,-16,-67,-68,64,-61,64,64,64,-76,-74,64,-63,-72,64,64,-85,-78,-82,64,-73,]),'WHILE':([6,12,21,26,32,36,38,39,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,95,109,110,130,139,154,155,156,161,163,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[-55,-56,-57,-58,-60,-59,65,65,65,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,65,-22,-23,65,-86,-64,65,-16,-67,-68,166,65,-61,65,65,65,-76,-74,65,-63,-72,65,65,-85,-78,-82,65,-73,]),'DO':([6,12,21,26,32,36,38,39,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,95,109,110,130,139,154,155,156,163,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[-55,-56,-57,-58,-60,-59,66,66,66,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,66,-22,-23,66,-86,-64,66,-16,-67,-68,66,-61,66,66,66,-76,-74,66,-63,-72,66,66,-85,-78,-82,66,-73,]),'RETURN':([6,12,21,26,32,36,38,39,45,47,48,49,50,51,52,53,54,55,56,57,59,60,69,74,95,109,110,130,139,154,155,156,163,168,169,171,176,179,181,182,185,186,188,191,192,193,194,195,197,],[-55,-56,-57,-58,-60,-59,67,67,67,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,67,-22,-23,67,-86,-64,67,-16,-67,-68,67,-61,67,67,67,-76,-74,67,-63,-72,67,67,-85,-78,-82,67,-73,]),'RBRACE':([6,12,21,26,32,36,38,44,45,46,47,48,49,50,51,52,53,54,55,56,57,59,60,69,73,74,95,110,130,139,154,155,156,168,169,176,179,181,185,186,188,192,193,194,195,197,],[-55,-56,-57,-58,-60,-59,-87,72,-87,-11,-22,-24,-25,-26,-27,-28,-29,-30,-31,-32,-33,-65,-66,94,-10,-22,-23,-86,-64,161,-16,-67,-68,-61,174,183,-76,-74,-63,-72,192,-85,-78,-82,196,-73,]),'COMMA':([16,25,35,88,89,90,91,93,96,101,102,103,121,122,123,124,150,157,],[22,31,41,-53,-54,-54,-54,22,41,134,-69,-71,-48,-49,-50,-51,-52,-70,]),'LPAREN':([17,19,20,58,61,62,63,64,65,67,75,78,79,81,92,108,111,112,113,114,115,116,117,118,119,120,134,136,166,172,],[23,24,-15,76,77,78,79,80,81,92,92,92,92,-79,92,92,92,92,92,92,92,92,92,92,92,92,92,92,172,92,]),'RPAREN':([23,24,27,28,30,35,40,42,59,60,76,84,85,86,87,88,89,90,91,96,99,100,101,102,103,104,121,122,123,124,125,128,130,135,138,140,141,142,143,144,145,146,147,148,149,150,157,160,168,170,177,184,185,],[-2,-87,33,34,-19,-87,-18,-21,-65,-66,-87,-34,-37,-42,-45,-53,-54,-54,-54,-87,131,132,133,-69,-71,-75,-48,-49,-50,-51,150,-20,-64,158,-80,-35,-36,-38,-39,-40,-41,-43,-44,-46,-47,-52,-70,165,-61,175,-84,190,-63,]),'LBRACE':([33,34,66,82,158,165,175,180,187,],[38,39,-83,109,163,171,182,-77,191,]),'ASSIGN':([58,106,],[75,75,]),'CTEF':([67,75,78,79,81,92,108,111,112,113,114,115,116,117,118,119,120,134,136,172,],[89,89,89,89,-79,89,89,89,89,89,89,89,89,89,89,89,89,89,89,89,]),'CTEI':([67,75,78,79,81,92,108,111,112,113,114,115,116,117,118,119,120,126,134,136,167,172,],[90,90,90,90,-79,90,90,90,90,90,90,90,90,90,90,90,90,152,90,90,152,90,]),'CTESTRING':([67,75,78,79,81,92,108,111,112,113,114,115,116,117,118,119,120,134,136,172,],[91,91,91,91,-79,91,91,91,91,91,91,91,91,91,91,91,91,91,91,91,]),'AND':([84,85,86,87,88,89,90,91,121,122,123,124,142,143,144,145,146,147,148,149,150,],[111,-37,-42,-45,-53,-54,-54,-54,-48,-49,-50,-51,-38,-39,-40,-41,-43,-44,-46,-47,-52,]),'OR':([84,85,86,87,88,89,90,91,121,122,123,124,142,143,144,145,146,147,148,149,150,],[112,-37,-42,-45,-53,-54,-54,-54,-48,-49,-50,-51,-38,-39,-40,-41,-43,-44,-46,-47,-52,]),'LT':([85,86,87,88,89,90,91,121,122,123,124,146,147,148,149,150,],[113,-42,-45,-53,-54,-54,-54,-48,-49,-50,-51,-43,-44,-46,-47,-52,]),'GT':([85,86,87,88,89,90,91,121,122,123,124,146,147,148,149,150,],[114,-42,-45,-53,-54,-54,-54,-48,-49,-50,-51,-43,-44,-46,-47,-52,]),'EQ':([85,86,87,88,89,90,91,121,122,123,124,146,147,148,149,150,],[115,-42,-45,-53,-54,-54,-54,-48,-49,-50,-51,-43,-44,-46,-47,-52,]),'NEQ':([85,86,87,88,89,90,91,121,122,123,124,146,147,148,149,150,],[116,-42,-45,-53,-54,-54,-54,-48,-49,-50,-51,-43,-44,-46,-47,-52,]),'PLUS':([86,87,88,89,90,91,121,122,123,124,148,149,150,],[117,-45,-53,-54,-54,-54,-48,-49,-50,-51,-46,-47,-52,]),'MINUS':([86,87,88,89,90,91,121,122,123,124,148,149,150,],[118,-45,-53,-54,-54,-54,-48,-49,-50,-51,-46,-47,-52,]),'TIMES':([87,88,89,90,91,121,122,123,124,150,],[119,-53,-54,-54,-54,-48,-49,-50,-51,-52,]),'DIVIDE':([87,88,89,90,91,121,122,123,124,150,],[120,-53,-54,-54,-54,-48,-49,-50,-51,-52,]),'LBRACKET':([93,137,162,],[126,126,167,]),'RBRACKET':([151,152,173,],[162,-62,178,]),'ELSE':([174,],[180,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'declaration_list':([4,38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[5,48,48,48,48,48,48,48,48,48,48,48,48,48,48,]),'declaration':([4,5,38,39,45,48,69,109,139,163,169,171,176,182,188,191,195,],[6,12,6,6,6,12,6,6,6,6,6,6,6,6,6,6,6,]),'tipo':([4,5,24,38,39,41,45,48,69,76,80,109,139,163,164,169,171,176,182,188,191,195,],[7,7,29,68,68,70,68,7,68,29,107,68,68,68,107,68,68,68,68,68,68,68,]),'function':([5,13,],[11,18,]),'functionF':([5,13,],[13,13,]),'empty':([5,13,24,35,38,45,76,96,],[14,14,30,42,46,46,30,42,]),'idFunc':([15,],[19,]),'declarationD':([22,31,],[26,36,]),'mainRef':([23,],[27,]),'parameter_list':([24,76,],[28,99,]),'bloque':([33,],[37,]),'parameter':([35,96,],[40,128,]),'bloqueB':([38,45,],[44,73,]),'statement_list':([38,39,45,109,163,171,182,191,],[45,69,45,139,169,176,188,195,]),'statement':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[47,47,74,95,47,95,47,95,47,95,47,95,47,95,]),'assignment_statement':([38,39,45,69,80,109,139,163,164,169,171,176,182,188,191,195,],[49,49,49,49,105,49,49,49,170,49,49,49,49,49,49,49,]),'read_statement':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,]),'write_statement':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[51,51,51,51,51,51,51,51,51,51,51,51,51,51,]),'if_statement':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[52,52,52,52,52,52,52,52,52,52,52,52,52,52,]),'for_statement':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[53,53,53,53,53,53,53,53,53,53,53,53,53,53,]),'while_statement':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[54,54,54,54,54,54,54,54,54,54,54,54,54,54,]),'do_while_statement':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[55,55,55,55,55,55,55,55,55,55,55,55,55,55,]),'return_statement':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[56,56,56,56,56,56,56,56,56,56,56,56,56,56,]),'callFunc':([38,39,45,69,109,139,163,169,171,176,182,188,191,195,],[57,57,57,57,57,57,57,57,57,57,57,57,57,57,]),'list_declaration':([38,39,45,69,80,109,139,163,164,169,171,176,182,188,191,195,],[59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,59,]),'matrix_declaration':([38,39,45,69,80,109,139,163,164,169,171,176,182,188,191,195,],[60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,60,]),'final':([43,],[71,]),'dowhile1':([66,],[82,]),'expression':([67,79,92,108,136,172,],[83,104,125,138,159,177,]),'exp1':([67,79,92,108,111,112,136,172,],[84,84,84,84,140,141,84,84,]),'exp':([67,75,79,92,108,111,112,113,114,115,116,117,118,136,172,],[85,98,85,85,85,85,85,142,143,144,145,146,147,85,85,]),'term':([67,75,79,92,108,111,112,113,114,115,116,117,118,119,120,136,172,],[86,86,86,86,86,86,86,86,86,86,86,86,86,148,149,86,86,]),'fact':([67,75,78,79,92,108,111,112,113,114,115,116,117,118,119,120,134,136,172,],[87,87,103,87,87,87,87,87,87,87,87,87,87,87,87,87,103,87,87,]),'debug':([71,],[97,]),'write_list':([78,],[101,]),'write_item':([78,134,],[102,157,]),'while1':([81,],[108,]),'addOp':([88,],[121,]),'addConst':([89,90,91,],[122,123,124,]),'dataObj':([97,],[129,]),'if2':([104,],[135,]),'var':([126,167,],[151,173,]),'terminaFunc':([127,],[153,]),'while2':([138,],[160,]),'condif':([174,],[179,]),'dowhile2':([177,],[184,]),'if3':([179,],[186,]),'if4':([180,],[187,]),'while3':([183,],[189,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID SEMICOLON declaration_list function MAIN LPAREN mainRef RPAREN bloque SEMICOLON final debug dataObj','program',14,'p_program','sintaxis.py',227),
  ('mainRef -> <empty>','mainRef',0,'p_mainRef','sintaxis.py',230),
  ('final -> <empty>','final',0,'p_final','sintaxis.py',236),
  ('debug -> <empty>','debug',0,'p_debug','sintaxis.py',244),
  ('dataObj -> <empty>','dataObj',0,'p_dataObj','sintaxis.py',251),
  ('tipo -> INT','tipo',1,'p_tipo','sintaxis.py',262),
  ('tipo -> FLOAT','tipo',1,'p_tipo','sintaxis.py',263),
  ('tipo -> STRING','tipo',1,'p_tipo','sintaxis.py',264),
  ('bloque -> LBRACE bloqueB RBRACE','bloque',3,'p_bloque','sintaxis.py',271),
  ('bloqueB -> statement_list bloqueB','bloqueB',2,'p_bloqueB','sintaxis.py',274),
  ('bloqueB -> empty','bloqueB',1,'p_bloqueB','sintaxis.py',275),
  ('function -> functionF function','function',2,'p_function','sintaxis.py',282),
  ('function -> empty','function',1,'p_function','sintaxis.py',283),
  ('functionF -> FUNC idFunc LPAREN parameter_list RPAREN LBRACE statement_list RBRACE SEMICOLON terminaFunc','functionF',10,'p_functionF','sintaxis.py',286),
  ('idFunc -> ID','idFunc',1,'p_idFunc','sintaxis.py',291),
  ('callFunc -> ID LPAREN parameter_list RPAREN SEMICOLON','callFunc',5,'p_callFunc','sintaxis.py',304),
  ('terminaFunc -> <empty>','terminaFunc',0,'p_terminaFunc','sintaxis.py',309),
  ('parameter_list -> tipo ID parameter','parameter_list',3,'p_parameter_list','sintaxis.py',317),
  ('parameter_list -> empty','parameter_list',1,'p_parameter_list','sintaxis.py',318),
  ('parameter -> COMMA tipo ID parameter','parameter',4,'p_parameter','sintaxis.py',325),
  ('parameter -> empty','parameter',1,'p_parameter','sintaxis.py',326),
  ('statement_list -> statement','statement_list',1,'p_statement_list','sintaxis.py',330),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','sintaxis.py',331),
  ('statement -> declaration_list','statement',1,'p_statement','sintaxis.py',339),
  ('statement -> assignment_statement','statement',1,'p_statement','sintaxis.py',340),
  ('statement -> read_statement','statement',1,'p_statement','sintaxis.py',341),
  ('statement -> write_statement','statement',1,'p_statement','sintaxis.py',342),
  ('statement -> if_statement','statement',1,'p_statement','sintaxis.py',343),
  ('statement -> for_statement','statement',1,'p_statement','sintaxis.py',344),
  ('statement -> while_statement','statement',1,'p_statement','sintaxis.py',345),
  ('statement -> do_while_statement','statement',1,'p_statement','sintaxis.py',346),
  ('statement -> return_statement','statement',1,'p_statement','sintaxis.py',347),
  ('statement -> callFunc','statement',1,'p_statement','sintaxis.py',348),
  ('expression -> exp1','expression',1,'p_expression','sintaxis.py',353),
  ('expression -> exp1 AND exp1','expression',3,'p_expression','sintaxis.py',354),
  ('expression -> exp1 OR exp1','expression',3,'p_expression','sintaxis.py',355),
  ('exp1 -> exp','exp1',1,'p_exp1','sintaxis.py',382),
  ('exp1 -> exp LT exp','exp1',3,'p_exp1','sintaxis.py',383),
  ('exp1 -> exp GT exp','exp1',3,'p_exp1','sintaxis.py',384),
  ('exp1 -> exp EQ exp','exp1',3,'p_exp1','sintaxis.py',385),
  ('exp1 -> exp NEQ exp','exp1',3,'p_exp1','sintaxis.py',386),
  ('exp -> term','exp',1,'p_exp','sintaxis.py',458),
  ('exp -> term PLUS exp','exp',3,'p_exp','sintaxis.py',459),
  ('exp -> term MINUS exp','exp',3,'p_exp','sintaxis.py',460),
  ('term -> fact','term',1,'p_term','sintaxis.py',490),
  ('term -> fact TIMES term','term',3,'p_term','sintaxis.py',491),
  ('term -> fact DIVIDE term','term',3,'p_term','sintaxis.py',492),
  ('fact -> ID addOp','fact',2,'p_fact','sintaxis.py',519),
  ('fact -> CTEF addConst','fact',2,'p_fact','sintaxis.py',520),
  ('fact -> CTEI addConst','fact',2,'p_fact','sintaxis.py',521),
  ('fact -> CTESTRING addConst','fact',2,'p_fact','sintaxis.py',522),
  ('fact -> LPAREN expression RPAREN','fact',3,'p_fact','sintaxis.py',523),
  ('addOp -> <empty>','addOp',0,'p_addOp','sintaxis.py',531),
  ('addConst -> <empty>','addConst',0,'p_addConst','sintaxis.py',543),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list','sintaxis.py',564),
  ('declaration_list -> declaration_list declaration','declaration_list',2,'p_declaration_list','sintaxis.py',565),
  ('declaration -> tipo ID SEMICOLON','declaration',3,'p_declaration','sintaxis.py',568),
  ('declaration -> tipo ID COMMA declarationD','declaration',4,'p_declaration','sintaxis.py',569),
  ('declarationD -> ID COMMA declarationD','declarationD',3,'p_declarationD','sintaxis.py',575),
  ('declarationD -> ID SEMICOLON','declarationD',2,'p_declarationD','sintaxis.py',576),
  ('list_declaration -> tipo ID LBRACKET var RBRACKET SEMICOLON','list_declaration',6,'p_list_declaration','sintaxis.py',588),
  ('var -> CTEI','var',1,'p_var','sintaxis.py',598),
  ('matrix_declaration -> tipo ID LBRACKET var RBRACKET LBRACKET var RBRACKET SEMICOLON','matrix_declaration',9,'p_matrix_declaration','sintaxis.py',603),
  ('assignment_statement -> ID ASSIGN exp SEMICOLON','assignment_statement',4,'p_assignment_statement','sintaxis.py',614),
  ('assignment_statement -> list_declaration','assignment_statement',1,'p_assignment_statement','sintaxis.py',615),
  ('assignment_statement -> matrix_declaration','assignment_statement',1,'p_assignment_statement','sintaxis.py',616),
  ('read_statement -> READ LPAREN ID RPAREN SEMICOLON','read_statement',5,'p_read_statement','sintaxis.py',635),
  ('write_statement -> WRITE LPAREN write_list RPAREN SEMICOLON','write_statement',5,'p_write_statement','sintaxis.py',646),
  ('write_list -> write_item','write_list',1,'p_write_list','sintaxis.py',649),
  ('write_list -> write_list COMMA write_item','write_list',3,'p_write_list','sintaxis.py',650),
  ('write_item -> fact','write_item',1,'p_write_item','sintaxis.py',653),
  ('if_statement -> IF LPAREN expression if2 RPAREN LBRACE statement_list RBRACE condif if3','if_statement',10,'p_if_statement','sintaxis.py',661),
  ('condif -> ELSE if4 LBRACE statement_list RBRACE SEMICOLON','condif',6,'p_condif','sintaxis.py',664),
  ('condif -> SEMICOLON','condif',1,'p_condif','sintaxis.py',665),
  ('if2 -> <empty>','if2',0,'p_if2','sintaxis.py',668),
  ('if3 -> <empty>','if3',0,'p_if3','sintaxis.py',676),
  ('if4 -> <empty>','if4',0,'p_if4','sintaxis.py',685),
  ('while_statement -> WHILE LPAREN while1 expression while2 RPAREN LBRACE statement_list RBRACE while3 SEMICOLON','while_statement',11,'p_while_statement','sintaxis.py',700),
  ('while1 -> <empty>','while1',0,'p_while1','sintaxis.py',703),
  ('while2 -> <empty>','while2',0,'p_while2','sintaxis.py',708),
  ('while3 -> <empty>','while3',0,'p_while3','sintaxis.py',719),
  ('do_while_statement -> DO dowhile1 LBRACE statement_list RBRACE WHILE LPAREN expression dowhile2 RPAREN SEMICOLON','do_while_statement',11,'p_do_while_statement','sintaxis.py',734),
  ('dowhile1 -> <empty>','dowhile1',0,'p_dowhile1','sintaxis.py',737),
  ('dowhile2 -> <empty>','dowhile2',0,'p_dowhile2','sintaxis.py',743),
  ('for_statement -> FOR LPAREN assignment_statement SEMICOLON expression SEMICOLON assignment_statement RPAREN LBRACE statement_list RBRACE','for_statement',11,'p_for_statement','sintaxis.py',754),
  ('return_statement -> RETURN expression SEMICOLON','return_statement',3,'p_return_statement','sintaxis.py',758),
  ('empty -> <empty>','empty',0,'p_empty','sintaxis.py',763),
]
