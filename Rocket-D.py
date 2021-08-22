from typing import Collection


class Expel_RD():
    #Diccionarios que guardan las variables de usuario:
    varCadena = {}
    varINT = {}
    varDecimal = {}
    #lista que almacena todos los errores
    errors = []

    def __init__(self, ruta): #CONSTRUCTOR
        # el construtor recibe la ruta del archivo
        archivo = open(ruta, 'r') # lee el archivo
        code = self.convertToList(archivo) # lo convierte en una lista bidimencional
        archivo.close()

        if (self.validador(code)): # se valida la sintaxis
            self.run(code)

    def run(self,code):
        #primer paso descomponer el archivo en una lista bidimencional
        
        #segundo paso identificar que tipo de funcion se debe ejecutar
        for line in range(0,len(code)):
            
            if(len(code[line]) != 0):
                if(code[line][0][0] == "@"): 
                    self.editVar(code[line])

                elif(code[line][0] == "vInt"): 
                    nameVar = code[line][1]
                    if(code[line][2] == "="):
                        valor = int(code[line][3])
                    else:
                        valor = 0
                    self.addVar(nameVar,valor,1)

                elif(code[line][0] == "vTxt"): 
                    nameVar = code[line][1]
                    if(code[line][2] == "="):
                        valor = self.comillasOut(code[line][3])
                    else:
                        valor = ""
                    
                    self.addVar(nameVar,valor,0)
                    
                
                elif(code[line][0] == "vFloat"): #para creacion de variables nuevas tipo entero
                    nameVar = code[line][1]
                    if(code[line][2] == "="):
                        valor = float(code[line][3])
                    else:
                        valor = 0.0
                    self.addVar(nameVar,valor,2)

                elif(code[line][0]== "showConsole"):
                    self.toPrint(code[line])

                elif(code[line][0] == "func"):
                    self.operacion(code[line])
                
                    
        

    #METODOS AUXILIARES
    def convertToList(self,archivoCodigo):
        return [linea.split() for linea in archivoCodigo]
        #este metodo convierte un archivo en una lista por linea y una lista con cada palabra sin espacios
    def comillasOut(self,text):
        return text[1:len(text)-1] # esto devuelve una cadena desde el index 1 hasta el penultimo elemento
    
    def arrobaOut(self,text):
        return text[1:] # devuelve un string sin el primer elemento
    
    #metodos para manejo de variables:
    def addVar(self,clave,valor,tipo):
        #considerando el 0 para tipo cadena 
        if(tipo == 0):
            self.varCadena[str(clave)] = str(valor)

        elif(tipo == 1): # el 1 para tipo entero
            
            self.varINT[str(clave)] = str(valor)

        elif(tipo == 2): # el 2 para tipo decimal
            
            self.varDecimal[str(clave)] = str(valor)
        
    
    

    def existVar(self,clave):
        if(str(clave) in self.varCadena):
            return True
        elif(str(clave) in self.varINT):
            return True
        elif(str(clave) in self.varDecimal):
            return True
        else:
            return False

    def varType(self,clave):
        if(str(clave) in self.varCadena):
            return 0
        elif(str(clave) in self.varINT):
            return 1
        elif(str(clave) in self.varDecimal):
            return 2

    def getVarData(self,clave):

        tipo = self.varType(clave)
        if(tipo == 0):    
            return self.varCadena[clave]
        elif(tipo == 1):
            return self.varINT[clave]
        elif(tipo == 2):
            return self.varDecimal[clave]   
    
    def editVar(self,codeLine):
        firtsVar = self.arrobaOut(codeLine[0])
            #evaluamos si lo que se quiere hacer es asignarle el valor de una variable a otra
        if(codeLine[2][0] == "@"):
            secondVar = self.arrobaOut(codeLine[2])
                #si la variable existe asigna el valor sino manda mensaje de error
            if(self.existVar(secondVar)):
                #se asigna el valor de la segunda variable a la primera, si la segunda existe
                self.varCadena[firtsVar] = self.getVarData(secondVar)
            else:
                    #la segunda variable no existe mandamos un error
                print("Error de asignacion", "La variable " + secondVar + " no esta definida")
        else:
            
            if(self.existVar(firtsVar)):
                
                type = self.varType(firtsVar)
                if(type == 0):
                    valor = self.comillasOut(codeLine[2])
                else:
                    valor = codeLine[2]
                
                self.addVar(firtsVar, valor,type)
            else:
                print("Error la variable " + firtsVar + " no esta definida")

    #metodo para imprimir cadena de texto
    def toPrint(self,codeLine):
        if(len(codeLine) > 2):
            textInicial = str(codeLine[1])[2:]
            lastText = str(codeLine[len(codeLine)-1])[:len(codeLine[len(codeLine)-1])-3]
            showText = textInicial
            for i in range(2,len(codeLine)-1):
                if (codeLine[i][0] == "@"):
                    nameVar= self.arrobaOut(codeLine[i])
                    dataVar = self.getVarData(nameVar)
                    showText = showText + " " + str(dataVar)
                else:
                    showText = showText + " " + str(codeLine[i])
            showText = showText + " " +  lastText
        else:
            lastTextIndex = len(codeLine[1])-3
            lastText=codeLine[1]
            showText = str(lastText[2:lastTextIndex])
        print(showText)
    #===========================
    # metodo para hacer operaciones
    def operacion(self,codeline):
        # recoger los datos necesarios:
        var = self.arrobaOut(codeline[1])
        num1 = codeline[3]
        num2 = codeline[5]
        operador = codeline[4]

        #verificar que los num sean numeros o variables
        
        if(num1[0] == '@'): # si lo que inicia es una arroba es porque es una variable
            varible1 = self.arrobaOut(num1)  # si es variable le quitamos el arroba 
            if ( self.existVar(varible1)): 
                num1 = self.getVarData(varible1) # si la variable existe conseguimos el dato en ella
                
        else:
            tipo = self.tipoEntrada(num1)
            if(tipo == "int"):
                num1 = int(num1) # si no es variable entonces convierte a entero el numero
            else:
                num1 = float(num1)

        if(num2[0] == '@'): # si lo que inicia es una arroba es porque es una variable
            varible2 = self.arrobaOut(num2)  # si es variable le quitamos el arroba 
            if ( self.existVar(varible2)): 
                num2 = self.getVarData(varible2) # si la variable existe conseguimos el dato en ella
        else:
            tipo = self.tipoEntrada(num1)
            if(tipo == "int"):
                num1 = int(num1) # si no es variable entonces convierte a entero el numero
            else:
                num1 = float(num1)
        
        if (operador == '+'):
            if(self.tipoEntrada(num1) == "int"):
                resultado = int(num1) + int(num2)
            else:
                resultado = round((float(num1) + float(num2)),2)
        elif(operador == '-'):
            if(self.tipoEntrada(num1) == "int"):
                resultado = int(num1) - int(num2)
            else:
                resultado = round((float(num1) - float(num2)),2)
        elif(operador == '/'):
            if(self.tipoEntrada(num1) == "int"):
                resultado = int(num1) / int(num2)
            else:
                resultado = round((float(num1) * float(num2)),2)
        elif(operador == '*'):
            if(self.tipoEntrada(num1) == "int"):
                resultado = int(num1) * int(num2)
            else:
                resultado = round((float(num1) / float(num2)),2)
        tipo = self.varType(var)
        
        self.addVar(var,resultado,tipo)

    #==================== VALIDADOR DE SINTAXIS
    def addError(self, lineError , message):
        self.errors.append(">>>>>>>>Error en la linea " + str(lineError + 1 ) + "\n             " + message)
    
    
    
    def validador(self, code):
        varTemp = {} 
        verificador = True  

        for line in range(0,len(code)):
            codeLine = code[line]
            firtsWord = codeLine[0]

            if(len(codeLine) != 0): # si la linea no esta vacia pasa a verificar
                
                if(firtsWord[0] == "@"): #para uso de variables ya declaradas

                    variable = self.arrobaOut(code[line][0])

                    if(len(codeLine) != 4): 
                        self.addError(line,"sintaxis incorrecta debe ir [@variable = valor ?]")
                        verificador = False

                    if(not variable in varTemp): #verifica que la variable ya fue declarada  
                        self.addError(line," la variable " + variable + " no esta declarada")
                        verificador = False

                    if(codeLine[len(codeLine)-1] != "?"): # verifica que el ultimo elemento sea ?
                        self.addError(line,"linea no terminada falta '?'")
                        verificador = False

                elif(firtsWord == "vInt" or firtsWord == "vFloat" or firtsWord == "vTxt"): #para creacion de variables nuevas
                    
                    if(len(codeLine) == 3):
                        if(codeLine[1] in varTemp):
                            self.addError(line,"La Variable ya estaba declarada")  
                            verificador = False
                        elif(firtsWord == "vInt"):
                            varTemp[codeLine[1]] = "int"
                        elif(firtsWord == "vFloat"):
                            varTemp[codeLine[1]] = "float"
                        elif(firtsWord == "vTxt"):
                            varTemp[codeLine[1]] = "text"
                        
                        if(codeLine[2] != "?"):
                            self.addError(line,"linea no terminada falta '?'")  
                            verificador = False

                    elif(len(codeLine) == 5):
                        if(not codeLine[1] in varTemp):
                            tipoVariable = self.tipoEntrada(codeLine[3])
                            
                            if(tipoVariable == "text"):
                                if(codeLine[3][0] != '"' and codeLine[3][ len(codeLine[3]) - 1 ] != '"'):
                                    self.addError(line,"los datos tipo texto deben estar entre comillas")
                                    verificador = False
                
                            varTemp[codeLine[1]] = tipoVariable
                        else:
                            self.addError(line,"La Variable ya estaba declarada")  
                            verificador = False

                        if(codeLine[4] != "?"):
                            self.addError(line,"linea no terminada falta '?'")  
                            verificador = False

                    else: 
                        self.addError(line,"Error en Sintaxis")  
                        verificador = False

                elif(firtsWord == "func"):
                    if(len(codeLine) == 7):
                        variable = self.arrobaOut(codeLine[1])
                        if(variable in varTemp):
                            num1 = codeLine[3]
                            num2 = codeLine[5]
                            if(num1[0] == '@'):
                                if( self.arrobaOut(num1) in varTemp):
                                    if(varTemp[self.arrobaOut(num1)] != varTemp[variable]):
                                        self.addError(line,"La Variable " + self.arrobaOut(num1) + " debe ser de tipo: " + varTemp[variable])  
                                        verificador = False
                                else:
                                    self.addError(line,"La Variable " + num1 + " no ha sido declarada")  
                                    verificador = False

                            elif(num2[0] == '@'):
                                if( self.arrobaOut(num2) in varTemp):
                                    if(varTemp[self.arrobaOut(num2)] != varTemp[variable]):
                                        self.addError(line,"La Variable " + self.arrobaOut(num2) + " debe ser de tipo: " + varTemp[variable])  
                                        verificador = False
                                else:
                                    self.addError(line,"La Variable " + num2 + " no ha sido declarada")  
                                    verificador = False  
                            
                            else:
                                tipo1 = self.tipoEntrada(num1)
                                tipo2 = self.tipoEntrada(num2)

                                if(varTemp[variable] != tipo1 and varTemp[variable] != tipo2 ):
                                    
                                    self.addError(line,"Los numeros deben ser del mismo tipo que la variable")  
                                    verificador = False

                        else:
                            self.addError(line,"La Variable " + variable + " no ha sido declarada")  
                            verificador = False

                        operadores = ("+","-","*","/")
                        if(codeLine[4] not in operadores):
                            self.addError(line,"El operador debe ser '+' o '-' o '*' o '/'")  
                            verificador = False
                    else:
                        self.addError(line,"Error en Sintaxis")  
                        verificador = False

        if(not verificador):
            print("ERROR-- el codigo no se ejecutara por los siguientes errores:")
            for x in self.errors:
                print(x)
            return False
        else:
            return True

    def tipoEntrada (self,entrada):
        try:
            float(entrada)
            if("." in entrada):
                tipo = "float"
            else:
                tipo = "int"
        except:
            tipo = "text"
        
        return tipo

#programa = Expel_RD('operacionesINT.txt')
#programa = Expel_RD('operacionesFloat.txt')
programa = Expel_RD('txtejemplos.txt')
