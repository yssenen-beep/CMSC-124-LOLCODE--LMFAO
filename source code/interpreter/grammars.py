from interpreter.tokens import TokenType

GRAMMAR_DEFINTIONS = {
    "<program>": [
        [TokenType.HAI, TokenType.LINEBREAK, "<var_section>", "<func_section>", TokenType.LINEBREAK, "<statements>", TokenType.LINEBREAK, TokenType.KTHXBYE]
    ],
    
    "<statement>": [
        ["<print>"],
        ["<input>"],
        ["<assignment>"],
        ["<recast>"],
        ["<expr>"],
        ["<switch_case>"],
        ["<if_else_block>"],
        ["<start_loop>"],
        [TokenType.GTFO]
    ],
    
    "<statements>": [
        ["<statement>"],
        ["<statements>", TokenType.LINEBREAK, "<statement>"]
    ],
    
    "<expr>": [
        ["<concatenation>"],
        ["<bool_allany>"],
        ["<operand>"]
    ],
    
    "<operand>": [
        ["<literal>"],
        [TokenType.IDENTIFIER], 
        ["<arithmetic>"],
        ["<comparison>"],
        ["<typecast>"],
        ["<func_call>"]
    ],

    # VARIABLES
    "<var_section>": [
        [TokenType.WAZZUP, TokenType.LINEBREAK, "<declarations>", TokenType.BUHBYE, TokenType.LINEBREAK],
        [] 
    ],
    
    "<declarations>": [
        ["<declaration>", TokenType.LINEBREAK, "<declarations>"],
        []
    ],
    
    "<declaration>": [
        [TokenType.I_HAS_A, TokenType.IDENTIFIER],
        [TokenType.I_HAS_A, TokenType.IDENTIFIER, TokenType.ITZ, "<expr>"]
    ],
    
    "<assignment>": [
        [TokenType.IDENTIFIER, TokenType.R, "<expr>"]
    ],

    # DATA TYPES
    "<literal>": [
        [TokenType.NUMBR],
        [TokenType.NUMBAR],
        [TokenType.YARN],
        [TokenType.TROOF]
    ],
    
    "<type>": [
        [TokenType.TYPE]
    ],

    # INPUT/OUTPUT
    "<print>": [
        [TokenType.VISIBLE, "<print_arg>"]
    ],
    
    "<print_arg>": [
        ["<print_arg>", TokenType.PLUS, "<expr>"],
        ["<expr>"]
    ],
    
    "<input>": [
        [TokenType.GIMMEH, TokenType.IDENTIFIER]
    ],

    # TYPECASTING
    "<recast>": [
        [TokenType.IDENTIFIER, TokenType.IS_NOW_A, "<type>"]
    ],
    
    "<typecast>": [
        [TokenType.MAEK, TokenType.IDENTIFIER, TokenType.A, "<type>"],
        [TokenType.MAEK, TokenType.IDENTIFIER, "<type>"]
    ],

    # SWITCH-CASE
    "<switch_case>": [
        [TokenType.WTF, TokenType.LINEBREAK, "<case_block>", TokenType.LINEBREAK, "<default_block>", TokenType.LINEBREAK, TokenType.OIC]
    ],
    
    "<case_block>": [
        ["<case>"],
        ["<case_block>", TokenType.LINEBREAK, "<case>"]
    ],
    
    "<case>": [
        [TokenType.OMG, "<literal>", TokenType.LINEBREAK, "<statements>", TokenType.GTFO]
    ],
    
    "<default_block>": [
        [TokenType.OMGWTF, TokenType.LINEBREAK, "<statements>"]
    ],

    # LOOPS
    "<start_loop>": [
        [TokenType.IM_IN_YR, TokenType.IDENTIFIER, "<operation>", "<condition>", TokenType.LINEBREAK, "<statements>", TokenType.LINEBREAK, TokenType.IM_OUTTA_YR, TokenType.IDENTIFIER]
    ],
    
    "<condition>": [
        [TokenType.TIL, "<expr>"],
        [TokenType.WILE, "<expr>"]
    ],
    
    "<operation>": [
        [TokenType.UPPIN, TokenType.YR, TokenType.IDENTIFIER],
        [TokenType.NERFIN, TokenType.YR, TokenType.IDENTIFIER]
    ],

    # FUNCTIONS
    "<func_section>": [
        [],  # ε (Empty)
        ["<func_section>", TokenType.LINEBREAK, "<func_dec>"]
    ],
    
    "<func_dec>": [
        [TokenType.HOW_IZ_I, TokenType.IDENTIFIER, "<params_line>", TokenType.LINEBREAK, "<statements>", TokenType.LINEBREAK, "<return_line>", TokenType.IF_U_SAY_SO]
    ],
    
    "<params_line>": [
        [],  # ε (Empty)
        ["<parameters>"]
    ],
    
    "<parameters>": [
        ["<parameter>"],
        ["<parameters>", TokenType.AN, "<parameter>"]
    ],
    
    "<parameter>": [
        [TokenType.YR, TokenType.IDENTIFIER]
    ],
    
    "<return_line>": [
        [],  # ε (Empty)
        [TokenType.FOUND_YR, "<expr>", TokenType.LINEBREAK]
    ],
    
    "<func_call>": [
        [TokenType.I_IZ, TokenType.IDENTIFIER, "<params_call_line>", TokenType.MKAY]
    ],
    
    "<params_call_line>": [
        [], 
        ["<params_call>"]
    ],
    
    "<params_call>": [
        ["<param_call>"],
        ["<params_call>", TokenType.AN, "<param_call>"]
    ],
    
    "<param_call>": [
        [TokenType.YR, "<expr>"]
    ],

    # IF-ELSE
    "<if_else_block>": [
        ["<bool_op>", TokenType.LINEBREAK, TokenType.O_RLY, TokenType.LINEBREAK, TokenType.YA_RLY, TokenType.LINEBREAK, "<statements>", TokenType.LINEBREAK, "<else_block>", TokenType.LINEBREAK, TokenType.OIC]
    ],
    
    "<else_block>": [
        ["<else>"],
        ["<else_if>"],
        ["<else_if>", "<else>"],
        []  # ε (Empty)
    ],
    
    "<else_if>": [
        [TokenType.MEBBE, "<bool_op>", TokenType.LINEBREAK, "<statements>"],
        [TokenType.MEBBE, "<bool_op>", TokenType.LINEBREAK, "<statements>", TokenType.LINEBREAK, "<else_if>"]
    ],
    
    "<else>": [
        [TokenType.NO_WAI, TokenType.LINEBREAK, "<statements>"]
    ],

    # BOOLEAN OPERATIONS
    "<bool_op>": [
        ["<bool_expr>"],
        ["<bool_allany>"]
    ],
    
    "<bool_expr>": [
        ["<bool>"],
        [TokenType.NOT, "<bool_expr>"],
        ["<binary_bool_ident>", "<bool_expr>", TokenType.AN, "<bool_expr>"]
    ],
    
    "<bool_allany>": [
        [TokenType.ALL_OF, "<bool_list>", TokenType.MKAY],
        [TokenType.ANY_OF, "<bool_list>", TokenType.MKAY]
    ],
    
    "<binary_bool_ident>": [
        [TokenType.BOTH_OF],
        [TokenType.EITHER_OF],
        [TokenType.WON_OF]
    ],
    
    "<bool_list>": [
        ["<bool_expr>", TokenType.AN, "<bool_expr>"],
        ["<bool_list>", TokenType.AN, "<bool_expr>"]
    ],
    
    "<bool>": [
        [TokenType.TROOF],
        [TokenType.IDENTIFIER],
        ["<comparison>"]
    ],

    # COMPARSION
    "<comparison>": [
        ["<comp_op>", "<num>", TokenType.AN, "<comp_expr>"]
    ],
    
    "<comp_op>": [
        [TokenType.BOTH_SAEM],
        [TokenType.DIFFRINT]
    ],
    
    "<comp_expr>": [
        ["<num>"],
        ["<rel_op>", "<num>", TokenType.AN, "<num>"]
    ],
    
    "<rel_op>": [
        [TokenType.BIGGR_OF],
        [TokenType.SMALLR_OF]
    ],

    # STRING CONCAT
    "<concatenation>": [
        [TokenType.SMOOSH, "<string_expr>"]
    ],
    
    "<string_expr>": [
        ["<string>"],
        ["<string_expr>", TokenType.AN, "<string>"]
    ],
    
    "<string>": [
        [TokenType.IDENTIFIER],
        [TokenType.YARN]
    ],

    # ARITHMETIC OPS
    "<arithmetic>": [
        ["<op>", "<math_expr>", TokenType.AN, "<math_expr>"]
    ],
    
    "<math_expr>": [
        ["<num>"],
        ["<arithmetic>"]
    ],
    
    "<num>": [
        [TokenType.NUMBR],
        [TokenType.NUMBAR],
        [TokenType.IDENTIFIER]
    ],
    
    "<op>": [
        [TokenType.SUM_OF],
        [TokenType.DIFF_OF],
        [TokenType.PRODUKT_OF],
        [TokenType.QUOSHUNT_OF],
        [TokenType.MOD_OF],
        [TokenType.BIGGR_OF],
        [TokenType.SMALLR_OF]
    ]
}
