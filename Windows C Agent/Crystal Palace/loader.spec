x64:
    load "loader.x64.o"
        make pic +gofirst
 
        dfr "resolve" "ror13"
        mergelib "libtcg.x64.zip"
 
        push $DLL
            link "my_data"
 
        export

