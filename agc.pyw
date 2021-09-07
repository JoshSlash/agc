# -*- coding: utf-8 -*-
# -*- coding: 1252 -*-
from tkinter import ttk
from tkinter import *
import os
import shutil
import csv
import codecs
import glob
import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from os import scandir
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def crearMatriz(anio):
	M=[]
	with open(anio+"/"+anio+".csv", newline='') as File:
			reader = csv.reader(File)
			for row in reader:
				M.append(row)
	return M

def reemplzar(A):
	for a in range(len(A)):
		for b in range(len(A[a])):
			if type(A[a][b])==type(A[a][b]):
				if A[a][b].find(","): A[a][b]=A[a][b].replace(",",".")

def darFormatoBD():	
	esp=["Nombre", "Nickname", "Genero", "Edad", "Direccion", "CP",	"Ciudad", "Estado", "Pais",	"E-mail", "Programa", "Profesion", "Fecha", "Contacto"]
	ing=["Name (As printed in your passport):*", "Preferred name (if different):*", "Gender*", "Age:*", "Permanent Address:*", "Zip Code:*", "City:*", "State/Province:*", "Country:*", "E-mail:*", "Name and dates of programs for which you are registering (if applicable):*","Tell us about your studies/the work you do:*", "When will you arrive in MEXICO City (Date, Approximate Hour)*", "How did you learn about CILAC FREIRE?*"]
	anno=["2017","2018","2019","2020","2021","2022","2023","2024","2025"]
	for i in anno:
		M=crearMatriz(i)
		#reemplzar(M)
		if len(M) > 0:
			for j in M:
				if len(j) < 12:
					M.remove(j)
			myData=M
			myFile = open(i+"/"+i+".csv", 'w')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(myData)

def lista_carpeta(path):
    return [obj.name for obj in scandir(path) if obj.is_file()]

def crearVentana(nombre):
	#Definicion de la ventana tk
	app = Tk()
	app.title(nombre)
	app.configure(background='#FAF3DD')
	app.wm_attributes("-alpha", 0.97)
	vp = Frame(app)
	vp.grid(column=0, row=0, padx=(90,90), pady=(30,30))
	vp.columnconfigure(0, weight=0)
	vp.rowconfigure(0, weight=1)
	vp.config(bg="#FAF3DD")
	return app,vp

def verBase(user):
	#darFormatoBD()
	esp=["Nombre", "Nickname", "Genero", "Edad", "Direccion", "CP",	"Ciudad", "Estado", "Pais",	"E-mail", "Programa", "Profesion", "Fecha", "Contacto"]
	esp2=["Nombre", "Nickname", "Genero", "Edad", "Direccion", "CP",	"Ciudad", "Estado", "Pais",	"E-mail", "Programa", "Profesion", "Fecha", "Contacto","Folio"," "," "]
	A=["2017","2018","2019","2020","2021","2022","2023","2024","2025"]
	L1=["Winter LGBTQ Program","Summer LGBTQ Program","Winter Women and Social Change in Mexico","Summer Women and Social Change in Mexico","Language and Culture for Educators","Medicine in Mexico: Prehispanic, Institutional, Alternative","Spanish Language for Ministry","Regular Program (all year-round)","COSECH","MONSKY","GSU"]
	L=["LGBTQW","LGBTQS","WOMENW","WOMENS","EDUCAT","MEDICI","MINIST","PSR","COSECH","MONSKY","GSU"]
	def generarPDF(M,anio):
		nombre=anio
		w, h = A4
		c = canvas.Canvas("Desktop/"+nombre+".pdf", pagesize=A4)
		for i in range(len(M)):
			text = c.beginText(50, h - 50)
			text.setFont("Times-Roman", 12)
			t=""
			for j in range(len(M[i])):
				if len(M[i])==0:
					continue
				t=text.textLine(M[i][j])
			c.drawText(text)
			c.showPage()	
		text.textLine("Este archivo se genero en: "+time.strftime("%d/%m/%y"))
		c.save()
		e1=Label(vp,text="Se genero correctamente el PDF de en Escritorio de su computadora",font='arial 14',fg="black", bg="#CFF1F7")
		e1.grid(column=1, row=101, sticky=(W,E))
	
	def regresar():
		app.destroy()
		menu(user)
	def actual():
		aniobb="2020"
		fecha=time.strftime("%d/%m/%y")
		for i in A:
			if fecha.find(i) > -1:
				aniobb=i
				break
		M=crearMatriz(aniobb)
		if len(M)>0: generarPDF(M,aniobb)
	def todo():
		for i in A:
			M=crearMatriz(i)
			#reemplzar(M)
			if len(M) > 0:
				generarPDF(M,i)

	app,vp=crearVentana("BASE DE DATOS DE ALUMNOS")
	Button(vp, text="Ver base de datos de año actual en PDF",font='arial 16',command=actual).grid(column=1, row=1)
	Button(vp, text="Ver base de datos completa en PDF",font='arial 16',command=todo).grid(column=1, row=2)
	Button(vp, text="Regresar",font='arial 16',command=regresar).grid(column=1, row=3)
	app.mainloop()

def validarNum(entrada):
	errorExcept=False
	try:
		dato=int(entrada)
	except:
		errorExcept=True
	return errorExcept

def validarDat(entrada):
	errorExcept=False
	try:
		dato=str(entrada)
	except:
		errorExcept=True
	return errorExcept

def convertirP(indice):
	M=["Winter LGBTQ Program","Summer LGBTQ Program","Winter Women and Social Change in Mexico","Summer Women and Social Change in Mexico","Language and Culture for Educators","Medicine in Mexico: Prehispanic, Institutional, Alternative","Spanish Language for Ministry","Regular Program (all year-round)"]
	return M[indice]

def formulario(user):
	anno=["2017","2018","2019","2020","2021","2022","2023","2024","2025"]
	L=["Winter LGBTQ Program","Summer LGBTQ Program","Winter Women and Social Change in Mexico","Summer Women and Social Change in Mexico","Language and Culture for Educators","Medicine in Mexico: Prehispanic, Institutional, Alternative","Spanish Language for Ministry","Regular Program (all year-round)","COSECH","MONSKY","GSU"]
	def cerrar():#Destruye la app formulario
		app.destroy()
		menu(user)
	def limpiar():#limpia cada caja de texto
		entrada1.delete(0,END)
		entrada2.delete(0,END)
		entrada3.delete(0,END)
		entrada4.delete(0,END)
		entrada5.delete(0,END)
		entrada6.delete(0,END)
		entrada7.delete(0,END)
		entrada8.delete(0,END)
		entrada9.delete(0,END)
		entrada10.delete(0,END)
		entrada11.delete(0,END)
		entrada12.delete(0,END)
		entrada13.delete(0,END)
		entrada14.delete(0,END)
	def hacer_click():#Ingreso a Base de datos desde archivo csv, la funcion write escribe dentro del archivo
		f=False
		S=[str(entrada1.get()),str(entrada2.get()),str(entrada3.get()),str(entrada4.get()),str(entrada5.get()),str(entrada6.get()),str(entrada7.get()),str(entrada8.get()),str(entrada9.get()),str(entrada10.get()),str(entrada11.get()),str(entrada12.get()),str(entrada13.get()),str(entrada14.get())]
		for k in range(len(anno)):
			if str(entrada13.get()).find(anno[k]) > -1:
				anio=anno[k]
				break
		archivo=open(anio+"/"+anio+".csv","a")
		archivo.write("\n")
		for i in range(len(S)):
			if len(S[i])==0:
				Label(vp,text='No se Guardaron los datos falta llenar un elemento >:(',font='arial 16').grid(column=1, row=15, sticky=(W,E))
				f=True
				break
		if f==False:
			for i in range(len(S)):
				archivo.write(S[i])
				if i == len(S): break
				archivo.write(",")
			archivo.write("\n")
			Label(vp,text='Se guardaron los datos correctamente',font="arial 16").grid(column=1, row=15, sticky=(W,E))
	#Definicion de la ventana tk
	app,vp=crearVentana("Formulario")
	#Creacion de botones y etiquetas
	v1=""
	e1=Label(vp,text='Nombre',font='arial 16 bold')
	e1.grid(column=1, row=1, sticky=(W,E))
	entrada1=Entry(vp, width=20, textvariable=v1,font="arial 16")
	entrada1.grid(column=2, row=1)
	v2=""
	e2=Label(vp,text='Nickname',font='arial 16 bold')
	e2.grid(column=1, row=2, sticky=(W,E))
	entrada2=Entry(vp, width=20, textvariable=v2,font="arial 16")
	entrada2.grid(column=2, row=2)
	v3=""
	e3=Label(vp,text='Genero',font='arial 16 bold')
	e3.grid(column=1, row=3, sticky=(W,E))
	entrada3=Entry(vp, width=20, textvariable=v3,font="arial 16")
	entrada3.grid(column=2, row=3)
	v4=""
	e4=Label(vp,text='Edad',font='arial 16 bold')
	e4.grid(column=1, row=4, sticky=(W,E))
	entrada4=Entry(vp, width=20, textvariable=v4,font="arial 16")
	entrada4.grid(column=2, row=4)
	v5=""
	e5=Label(vp,text='Direccion',font='arial 16 bold')
	e5.grid(column=1, row=5, sticky=(W,E))
	entrada5=Entry(vp, width=20, textvariable=v5,font="arial 16")
	entrada5.grid(column=2, row=5)
	v6=""
	e6=Label(vp,text='CP',font='arial 16 bold')
	e6.grid(column=1, row=6, sticky=(W,E))
	entrada6=Entry(vp, width=20, textvariable=v6,font="arial 16")
	entrada6.grid(column=2, row=6)
	v7=""
	e7=Label(vp,text='Ciudad',font='arial 16 bold')
	e7.grid(column=1, row=7, sticky=(W,E))
	entrada7=Entry(vp, width=20, textvariable=v7,font="arial 16")
	entrada7.grid(column=2, row=7)
	v8=""
	e8=Label(vp,text='Estado',font='arial 16 bold')
	e8.grid(column=1, row=8, sticky=(W,E))
	entrada8=Entry(vp, width=20, textvariable=v8,font="arial 16")
	entrada8.grid(column=2, row=8)
	v9=""
	e9=Label(vp,text='Pais',font='arial 16 bold')
	e9.grid(column=1, row=9, sticky=(W,E))
	entrada9=Entry(vp, width=20, textvariable=v9,font="arial 16")
	entrada9.grid(column=2, row=9)
	v10=""
	e10=Label(vp,text='E-mail',font='arial 16 bold')
	e10.grid(column=1, row=10, sticky=(W,E))
	entrada10=Entry(vp, width=20, textvariable=v10,font="arial 16")
	entrada10.grid(column=2, row=10)
	v11=""
	e11=Label(vp,text='Programa',font='arial 16 bold')
	e11.grid(column=1, row=11, sticky=(W,E))
	entrada11=Entry(vp, width=20, textvariable=v11,font="arial 16")
	entrada11.grid(column=2, row=11)
	v12=""
	e12=Label(vp,text='Profesion',font='arial 16 bold')
	e12.grid(column=1, row=12, sticky=(W,E))
	entrada12=Entry(vp, width=20, textvariable=v12,font="arial 16")
	entrada12.grid(column=2, row=12)
	v13=""
	e13=Label(vp,text='Fecha de llegada',font='arial 16 bold')
	e13.grid(column=1, row=13, sticky=(W,E))
	entrada13=Entry(vp, width=20, textvariable=v13,font="arial 16")
	entrada13.grid(column=2, row=13)
	v14=""
	e14=Label(vp,text='Cómo nos contacto',font='arial 16 bold')
	e14.grid(column=1, row=14, sticky=(W,E))
	entrada14=Entry(vp, width=20, textvariable=v14,font="arial 16")
	entrada14.grid(column=2, row=14)
	boton = Button(vp, text="Guardar",font='arial 16',command=hacer_click)
	boton.grid(column=2, row=17)
	botonLimpiar = Button(vp, text="Nuevo",font='arial 16', command=limpiar)
	botonLimpiar.grid(column=1, row=17)
	botonCerrar = Button(vp, text="Regresar",font='arial 16',command=cerrar)
	botonCerrar.grid(column=3, row=17)
	app.mainloop()

def menu(user):
	def buscarfolio():
		app.destroy()
		botonBuscarFolio()
	def buscar():#Abre menu buscar
		app.destroy()
		botonBuscar(user)
	def nuevo():#Abre menu formulario
		app.destroy()
		formulario(user)
	def salir():#Sale de la app menu
		app.destroy()
	def borrar():
		app.destroy()
		botonEliminar()
	def update():
		app.destroy()
		botonActualizar()
	def archivo():
		app.destroy()
		botonCargar(user)
	def anno():#Abre menu formulario
		app.destroy()
		anno2()
	def bd():
		app.destroy()
		verBase(user)
	def generalHAdmin():
		app.destroy()
		ayudaAdmin()
	def generalHCline():
		app.destroy()
		ayudaClient()

	app,vp=crearVentana("Menu")
	if user==1:
		texto=["Cargar Archivo","Nuevo Alumno","Actualizar Alumno","Borrar Alumo","Buscar Alumno","Agregar Folio a Alumno", "Imprimir Base de datos","Salir"]
		color=['#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7','#CFF1F7']
		botones=[archivo,nuevo,update,borrar,buscar,anno,bd,salir]
		for i in range(len(texto)):
			B=Button(vp,text=texto[i],font='arial 20',command=botones[i],bg=color[i])
			B.grid(column=1, row=i+1)
	else:
		texto2=["Cargar Archivo","Nuevo Registro","Buscar Alumno","Ver BD Actual","Salir"]
		botones2=[archivo,nuevo,buscar,bd,salir]
		color=['#FFB6C1','#E6E6FA','#00FF00','#F0E68C','#FFA07A','#FFE4E1']
		for i in range(len(texto2)):
			B=Button(vp,text=texto2[i],font='arial 20',command=botones2[i],bg=color[i])
			B.grid(column=1, row=i+1)
	app.mainloop()

def ayudaAdmin():
	def cargarHepl():
		def cerraH():
			app.destroy()
		app,vp=crearVentana("Ayuda Cargar Archivo")
		vE=""
		e1=Label(vp,text="1) Para cargar la base de datos solo ingrese el año donde se guardará")
		e1.grid(column=1, row=1, sticky=(W,E))
		e2=Label(vp,text="2) Al teminar precione regresar para volver al menu principal")
		e2.grid(column=1, row=2, sticky=(W,E))
		Button(vp, text="Regresar", command=cerraH).grid(column=1, row=3)
		app.mainloop()

	def formHelp():
		def cerraH():
			app.destroy()
		app,vp=crearVentana("Ayuda Nuevo Registro")
		vE=""
		e1=Label(vp,text="1) Para ingresar un nuevo registro llene los datos requeridos y precione el boton Guardar")
		e1.grid(column=1, row=1, sticky=(W,E))
		e2=Label(vp,text="2) Si desea agregar varios registros, precione el boton Nuevo y se limpiaran los campos de texto")
		e2.grid(column=1, row=2, sticky=(W,E))
		Button(vp, text="Regresar", command=cerraH).grid(column=1, row=3)
		app.mainloop()

	def actHelp():
		def cerraH():
			app.destroy()
		app,vp=crearVentana("Ayuda Actualizar Alumno")
		vE=""
		e1=Label(vp,text="1) Para actualizar un registro deberá ingresar el nombre completo como se registro")
		e1.grid(column=1, row=1, sticky=(W,E))
		e2=Label(vp,text="2) Seleccionar el año en el que vino o está regristrado en la base de datos")
		e2.grid(column=1, row=2, sticky=(W,E))
		e3=Label(vp,text="3) Seleccionar el programa al que se inscribió")
		e3.grid(column=1, row=3, sticky=(W,E))
		e4=Label(vp,text="4) Seleccionar el dato que se desea actualizar, recuerde que es un dato a la vez")
		e4.grid(column=1, row=4, sticky=(W,E))
		Button(vp, text="Regresar", command=cerraH).grid(column=1, row=5)
		app.mainloop()

	def borrarH():
		def cerraH():
			app.destroy()
		app,vp=crearVentana("Ayuda Borrar Alumno")
		vE=""
		e1=Label(vp,text="1) Para borar un registro deberá ingresar el nombre completo como se registro")
		e1.grid(column=1, row=1, sticky=(W,E))
		e2=Label(vp,text="2) Seleccionar el año en el que vino o esta regristrado en la base de datos")
		e2.grid(column=1, row=2, sticky=(W,E))
		e3=Label(vp,text="3) Seleccionar el programa al que se inscribió")
		e3.grid(column=1, row=3, sticky=(W,E))
		e4=Label(vp,text="4) Seleccionar el dato que se desea actualizar,recuerde que es un dato a la vez")
		e4.grid(column=1, row=4, sticky=(W,E))
		Button(vp, text="Regresar", command=cerraH).grid(column=1, row=5)
		app.mainloop()

	def buscarH():
		def cerraH():
			app.destroy()
		app,vp=crearVentana("Ayuda Buscar Alumno")
		vE=""
		e1=Label(vp,text="1) Para buscar un registro deberá ingresar el nombre completo como se registro")
		e1.grid(column=1, row=1, sticky=(W,E))
		e2=Label(vp,text="2) Seleccionar el año en el que vino o esta regristrado en la base de datos")
		e2.grid(column=1, row=2, sticky=(W,E))
		e3=Label(vp,text="3) Seleccionar el programa al que se inscribió")
		e3.grid(column=1, row=3, sticky=(W,E))
		e4=Label(vp,text="4) Seleccionar el dato que se desea actualizar,recuerde que es un dato a la vez")
		e4.grid(column=1, row=4, sticky=(W,E))
		Button(vp, text="Regresar", command=cerraH).grid(column=1, row=5)
		app.mainloop()

	def regresarM():
		app.destroy()
		menu(1)

	app,vp=crearVentana("Ayuda AGC")
	texto=["Cargar","Nuevo Registro","Actualizar","Borrar Registro","Buscar","Regresar"]
	botones=[cargarHepl,formHelp,actHelp,borrarH,buscarH,regresarM]
	for i in range(len(texto)):
		B=Button(vp,text=texto[i],font='arial 12',command=botones[i])
		B.grid(column=1, row=i+1)
	app.mainloop()

def ayudaClient():
	def cargarHepl():
		def cerraH():
			app.destroy()
		app,vp=crearVentana("Ayuda Cargar Archivo")
		vE=""
		e1=Label(vp,text="1) Para cargar la base de datos solo ingrese el año donde se guardará")
		e1.grid(column=1, row=1, sticky=(W,E))
		e2=Label(vp,text="2) Al teminar precione regresar para volver al menu principal")
		e2.grid(column=1, row=2, sticky=(W,E))
		Button(vp, text="Regresar", command=cerraH).grid(column=1, row=3)
		app.mainloop()

	def formHelp():
		def cerraH():
			app.destroy()
		app,vp=crearVentana("Ayuda Nuevo Registro")
		vE=""
		e1=Label(vp,text="1) Para ingresar un nuevo registro llene los datos requeridos y precione el boton Guardar")
		e1.grid(column=1, row=1, sticky=(W,E))
		e2=Label(vp,text="2) Si desea agregar varios registros, precione el boton Nuevo y se limpiaran los campos de texto")
		e2.grid(column=1, row=2, sticky=(W,E))
		Button(vp, text="Regresar", command=cerraH).grid(column=1, row=3)
		app.mainloop()

	def buscarH():
		def cerraH():
			app.destroy()
		app,vp=crearVentana("Ayuda Buscar Alumno")
		vE=""
		e1=Label(vp,text="1) Para buscar un registro deberá ingresar el nombre completo como se registro")
		e1.grid(column=1, row=1, sticky=(W,E))
		e2=Label(vp,text="2) Seleccionar el año en el que vino o esta regristrado en la base de datos")
		e2.grid(column=1, row=2, sticky=(W,E))
		e3=Label(vp,text="3) Seleccionar el programa al que se inscribió")
		e3.grid(column=1, row=3, sticky=(W,E))
		e4=Label(vp,text="4) Seleccionar el dato que se desea actualizar,recuerde que es un dato a la vez")
		e4.grid(column=1, row=4, sticky=(W,E))
		Button(vp, text="Regresar", command=cerraH).grid(column=1, row=5)
		app.mainloop()

	def regresarM():
		app.destroy()
		menu(2)

	app,vp=crearVentana("Ayuda AGC")
	texto=["Cargar","Nuevo Registro","Buscar","Regresar"]
	botones=[cargarHepl,formHelp,buscarH,regresarM]
	for i in range(len(texto)):
		B=Button(vp,text=texto[i],font='arial 12',command=botones[i])
		B.grid(column=1, row=i+1)
	app.mainloop()

def anno2():
	esp=["Nombre", "Nickname", "Genero", "Edad", "Direccion", "CP",	"Ciudad", "Estado", "Pais",	"E-mail", "Programa", "Profesion", "Fecha", "Contacto"]
	A=["2017","2018","2019","2020","2021","2022","2023","2024","2025"]
	L1=["Winter LGBTQ Program","Summer LGBTQ Program","Winter Women and Social Change in Mexico","Summer Women and Social Change in Mexico","Language and Culture for Educators","Medicine in Mexico: Prehispanic, Institutional, Alternative","Spanish Language for Ministry","Regular Program (all year-round)","COSECH","MONSKY","GSU"]
	L=["LGBTQW","LGBTQS","WOMENW","WOMENS","EDUCAT","MEDICI","MINIST","PSR","COSECH","MONSKY","GSU"]
	aniobb=0
	def salir():#sale de menu buscar
		app.destroy()
		menu(1)
	def act():
		alumno=[]
		def salir2():#sale de menu buscar
			app2.destroy()
		app2,vp2=crearVentana("Agregar anio y folio a Alumno")
		for i in range(len(esp)):
			e1=Label(vp2,text=esp[i],font='arial 12 bold',fg="black", bg="#CFF1F7")
			e1.grid(column=1, row=i, sticky=(W,E))
		n=str(entrada1.get())
		c=2
		count=0
		for i in A:
			M=crearMatriz(i)
			#reemplzar(M)
			if len(M)>0:
				for j in range(len(M)):
					esta=False
					for k in range (len(M[j])):
						if M[j][k].find(n) > -1:
							esta=True
					if (esta):
						count+=1
						alumno=M[j]
						aniobb=i
						for l in range(len(M[j])):
							e1=Label(vp2,text=M[j][l],font='arial 12',fg="black", bg="#CFF1F7")
							e1.grid(column=c, row=l, sticky=(W,E))
						c+=1
		Button(vp2, text="Regresar",font='arial 20',command=salir2).grid(column=3, row=100)
		if (count==1):
			def actualizarAlumno():
				v1=""
				v2=""
				app3,vp3=crearVentana("Agregar Folio: "+alumno[0])
				Label(vp3,text="Folio: ",font='arial 16 bold').grid(column=1, row=1, sticky=(W,E))
				entrada1=Entry(vp3, width=20, textvariable=v1,font="arial 16")
				entrada1.grid(column=2, row=1)
				opcion=""
				def salirs(): app3.destroy()
				def select():
					M=crearMatriz(aniobb)
				#	reemplzar(M)
					M.remove(alumno)
					alumno.append(str(entrada1.get()))
					M.append(alumno)
					myData=M
					myFile = open(aniobb+"/"+aniobb+".csv", 'w')
					with myFile:
						writer = csv.writer(myFile)
						writer.writerows(myData)
					Label(vp3,text="Se actualizo correctamente el folio: "+str(entrada1.get()),font='arial 16 bold').grid(column=1, row=3, sticky=(W,E))
					Button(vp3, text="Salir",font='arial 20',command=salirs).grid(column=2, row=3)				
				Button(vp3, text="Agregar folio: "+alumno[0],font='arial 20',command=select).grid(column=1, row=2)
				Button(vp3, text="Cancelar",font='arial 20',command=salirs).grid(column=1, row=2)
			Button(vp2, text="Agregar Folio",font='arial 20',command=actualizarAlumno).grid(column=1, row=100)
		else:
			e1=Label(vp2,text="¡Siga buscando su alumno!",font='arial 14',fg="black", bg="#CFF1F7")
			e1.grid(column=1, row=100, sticky=(W,E))
		app2.mainloop()
	app,vp=crearVentana("Actualizar Alumno")
	v12=IntVar()
	v12.set(1)
	v13=IntVar()
	v13.set(1)
	v1=""
	e1=Label(vp,text="Ingrese Nombre del alumno a buscar:",font='arial 20 bold',fg="black", bg="#CFF1F7")
	e1.grid(column=1, row=1, sticky=(W,E))
	entrada1=Entry(vp, width=20, textvariable=v1,font='arial 20')
	entrada1.grid(column=1, row=2)
	Button(vp, text="Buscar",font='arial 20',command=act).grid(column=1, row=3)
	Button(vp, text="Regresar",font='arial 20',command=salir).grid(column=1, row=4)
	app.mainloop()

def addAnno(M,ano,nombre,correo):
	def nou():
			app.destroy()
	def yes():
		app.destroy()
		addFolio(M,ano,nombre,correo)
	def salir():#sale de menu buscar
		app.destroy()

	def revisar():
		for i in range(len(M)):
			if (str(nombre) in M[i]):
				if (str(correo) in M[i]):
					return i
		return 0
	fila=revisar()
	def act():
		def no():
			app.destroy()
		def si():
			app.destroy()
			addFolio(M,ano,nombre,correo)
		if len(M[fila])<=14:
			M[fila].append(str(entrada1.get()))
			myData=M
			myFile = open(ano+"/"+ano+".csv", 'w')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(myData)
			l=Label(vp,text="Se Actualizo el dato Correcatamente =D",font='arial 12 bold')
			l.grid(column=2, row=2, sticky=(W,E))
			Button(vp, text="Cerrar",font='arial 12 bold',command=salir).grid(column=1, row=3)
		if len(M[fila])>14:
			l=Label(vp,text="El alumno ya tiene Año: ¿Agregar folio a "+nombre+"?",font='arial 12 bold')
			l.grid(column=1, row=3, sticky=(W,E))
			Button(vp, text="No lo hare despues",font='arial 12 bold',command=no).grid(column=2, row=3)
			Button(vp, text="Si",font='arial 12 bold',command=si).grid(column=3, row=3)
	app,vp=crearVentana("Alumno")
	if (fila!=0):
		if len(M[fila])==14:
			v1=""
			Label(vp,text="Agregue el año de registro del alumno:").grid(column=1, row=1, sticky=(W,E))
			entrada1=Entry(vp, width=20, textvariable=v1)
			entrada1.grid(column=2, row=1)
			Button(vp, text="Agregar año",font='arial 12',command=act).grid(column=1, row=2)
		if len(M[fila])==15:
			l=Label(vp,text="El alumno ya tiene Año: ¿Agregar folio a "+nombre+"?",font='arial 12 bold')
			l.grid(column=1, row=1, sticky=(W,E))
			Button(vp, text="No lo hare despues",font='arial 12 bold',command=nou).grid(column=1, row=2)
			Button(vp, text="Si",font='arial 12 bold',command=yes).grid(column=2, row=2)
		if len(M[fila])==16:
			e1=Label(vp,text="El alumno ya tiene año y Folio",font='arial 12 bold')
			e1.grid(column=1, row=1, sticky=(W,E))
			Button(vp, text="Regresar",font='arial 12',command=salir).grid(column=1, row=2)
	else:
		v1=""
		e1=Label(vp,text="No se pudo buscar "+nombre+" Porque no se encuentra el alumno, revice el nombre e intente de nuevo",font='arial 12 bold')
		e1.grid(column=1, row=1, sticky=(W,E))
		Button(vp, text="Regresar",font='arial 12',command=salir).grid(column=1, row=2)
	app.mainloop()

def addFolio(M,ano,nombre,correo):
	def salir():#sale de menu buscar
		app.destroy()
	def revisar():
		for i in range(len(M)):
			if (str(nombre) in M[i]):
				if (str(correo) in M[i]):
					return i
		return 0
	fila=revisar()
	def act():
		if len(M[fila])==15:
			M[fila].append(str(entrada1.get()))
			myData=M
			myFile = open(ano+"/"+ano+".csv", 'w')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(myData)
			l=Label(vp,text="Se Actualizo el dato Correcatamente =D",font='arial 12 bold')
			l.grid(column=2, row=2, sticky=(W,E))
		if len(M[fila])>15:
			l=Label(vp,text="Ya tiene folio el alumno",font='arial 12 bold')
			l.grid(column=2, row=2, sticky=(W,E))
		Button(vp, text="Cerrar",font='arial 12',command=salir).grid(column=1, row=3)
	def regresar():
		app.destroy()

	app,vp=crearVentana("Alumno")
	if (fila!=0):
		if len(M[fila])==15:
			v1=""
			Label(vp,text="Agregue el folio del alumno:").grid(column=1, row=1, sticky=(W,E))
			entrada1=Entry(vp, width=20, textvariable=v1)
			entrada1.grid(column=2, row=1)
			Button(vp, text="Actualizar",font='arial 12',command=act).grid(column=1, row=2)
		else:
			Label(vp,text="El alumno ya tiene folio y año").grid(column=1, row=1, sticky=(W,E))
			Button(vp, text="Regresar",font='arial 12',command=regresar).grid(column=1, row=2)
	else:
		v1=""
		e1=Label(vp,text="No se pudo buscar "+nombre+" Porque no se encuentra el alumno, revice el nombre e intente de nuevo",font='arial 12 bold')
		e1.grid(column=1, row=1, sticky=(W,E))
		Button(vp, text="Regresar",font='arial 12',command=salir).grid(column=1, row=2)
	app.mainloop()

def validar(user):
	def entrar():#Valida y entra solo con la contrasenia y usuario
		if user==1:
			if str(entrada1.get())=="JTV2015CILAC":
				if str(entrada2.get())=="Paulo15Freire":
					app.destroy()
					menu(1)
		if user==2:
			if str(entrada1.get())=="CIL2018PF":
				if str(entrada2.get())=="Freire15Paulo":
					app.destroy()
					menu(2)

	def salir():#Sale de la app validar
		app.destroy()

	def regreso():#Abre menu usuario
		app.destroy()
		usuario()
	#Definicion de la ventana tk
	app,vp=crearVentana("Validacion")
	#Creacion de botones y etiquetas
	v1=""
	e1=Label(vp,text='Usuario',font='arial 16 bold')
	e1.grid(column=1, row=1, sticky=(W,E))
	entrada1=Entry(vp, width=20, textvariable=v1,font='arial 16')
	entrada1.grid(column=2, row=1)
	v2=""
	e2=Label(vp,text='Contraseña',font='arial 16 bold')
	e2.grid(column=1, row=2, sticky=(W,E))
	entrada2=Entry(vp, width=20, textvariable=v2,show='*',font='arial 16')
	entrada2.grid(column=2, row=2)

	botonEntrar=Button(vp, text="Entrar",font='arial 16',command=entrar,bg='#00FF00')
	botonEntrar.grid(column=1, row=3)
	botonSalir=Button(vp, text="Salir",font='arial 16',command=salir,bg='#DCDCDC')
	botonSalir.grid(column=3, row=3)
	botonRegresar=Button(vp, text="Regresar",font='arial 16',command=regreso,bg='#FFE4E1')
	botonRegresar.grid(column=2, row=3)
	app.mainloop()

def usuario():
	def admin():#Sale de menu usuario y abre menu validar
		app2.destroy()
		validar(1)
	def user():
		app2.destroy()
		validar(2)
	def crear():
		pass
	def salir():#Sale de menu usuario
		app2.destroy()
	#Definicion de la ventana tk
	app2,vp2=crearVentana("Usuarios")
	#Creacion de botones y etiquetas
	botonAdmin=Button(vp2, text="Adimnistrador",font='arial 16',command=admin,bg='#FFB6C1')
	botonAdmin.grid(column=1, row=1)
	botonUsuario=Button(vp2, text="Usuario",font='arial 16',command=user,bg='#FFE4E1')
	botonUsuario.grid(column=1, row=2)
	botonSalir=Button(vp2, text="Salir",font='arial 16',command=salir,bg='#DCDCDC')
	botonSalir.grid(column=1, row=4)
	Label(vp2,text=time.strftime("%d/%m/%y"),font='arial 14 bold',fg="black", bg="#CFF1F7").grid(column=1, row=5, sticky=(W,E))
	app2.mainloop()

def botonBuscar(user):
	esp=["Nombre", "Nickname", "Genero", "Edad", "Direccion", "CP",	"Ciudad", "Estado", "Pais",	"E-mail", "Programa", "Profesion", "Fecha", "Contacto"]
	A=["2017","2018","2019","2020","2021","2022","2023","2024","2025"]
	L1=["Winter LGBTQ Program","Summer LGBTQ Program","Winter Women and Social Change in Mexico","Summer Women and Social Change in Mexico","Language and Culture for Educators","Medicine in Mexico: Prehispanic, Institutional, Alternative","Spanish Language for Ministry","Regular Program (all year-round)","COSECH","MONSKY","GSU"]
	L=["LGBTQW","LGBTQS","WOMENW","WOMENS","EDUCAT","MEDICI","MINIST","PSR","COSECH","MONSKY","GSU"]
	def salir():#sale de menu buscar
		app.destroy()
		menu(1)
	def act():
		alumno=[]
		def salir2():#sale de menu buscar
			app2.destroy()
		app2,vp2=crearVentana("Buscar Alumno")
		for i in range(len(esp)):
			e1=Label(vp2,text=esp[i],font='arial 12 bold',fg="black", bg="#CFF1F7")
			e1.grid(column=1, row=i, sticky=(W,E))
		n=str(entrada1.get())
		c=2
		count=0
		for i in A:
			M=crearMatriz(i)
			#reemplzar(M)
			if len(M)>0:
				for j in range(len(M)):
					esta=False
					for k in range (len(M[j])):
						if M[j][k].find(n) > -1:
							esta=True
					if (esta):
						count+=1
						alumno=M[j]
						for l in range(len(M[j])):
							e1=Label(vp2,text=M[j][l],font='arial 12',fg="black", bg="#CFF1F7")
							e1.grid(column=c, row=l, sticky=(W,E))
						c+=1
		Button(vp2, text="Regresar",font='arial 20',command=salir2).grid(column=3, row=100)
		if (count==1):
			def generarPDF():
				nombre=alumno[0]
				w, h = A4
				c = canvas.Canvas("Desktop/"+nombre+".pdf", pagesize=A4)
				text = c.beginText(50, h - 50)
				text.setFont("Times-Roman", 12)
				for i in range(len(esp)):
					text.textLine(esp[i]+":"+"    "+alumno[i])
				c.drawText(text)
				c.showPage()
				c.save()
				e1=Label(vp2,text="Se genero correctamente el PDF de "+nombre+" en Escritorio de su computadora",font='arial 14',fg="black", bg="#CFF1F7")
				e1.grid(column=1, row=101, sticky=(W,E))
			Button(vp2, text="Generar PDF",font='arial 20',command=generarPDF).grid(column=1, row=100)
		else:
			e1=Label(vp2,text="¡Siga buscando su alumno!",font='arial 14',fg="black", bg="#CFF1F7")
			e1.grid(column=1, row=100, sticky=(W,E))
		app2.mainloop()
	app,vp=crearVentana("Buscar Alumno")
	v12=IntVar()
	v12.set(1)
	v13=IntVar()
	v13.set(1)
	v1=""
	e1=Label(vp,text="Ingrese Nombre del alumno a buscar:",font='arial 20 bold',fg="black", bg="#CFF1F7")
	e1.grid(column=1, row=1, sticky=(W,E))
	entrada1=Entry(vp, width=20, textvariable=v1,font='arial 20')
	entrada1.grid(column=1, row=2)
	Button(vp, text="Buscar",font='arial 20',command=act).grid(column=1, row=3)
	Button(vp, text="Regresar",font='arial 20',command=salir).grid(column=1, row=4)
	app.mainloop()

def botonCargar(user):
	esp=["Nombre", "Nickname", "Genero", "Edad", "Direccion", "CP",	"Ciudad", "Estado", "Pais",	"E-mail", "Programa", "Profesion", "Fecha", "Contacto"]
	ing=["Name (As printed in your passport):*", "Preferred name (if different):*", "Gender*", "Age:*", "Permanent Address:*", "Zip Code:*", "City:*", "State/Province:*", "Country:*", "E-mail:*", "Name and dates of programs for which you are registering (if applicable):*","Tell us about your studies/the work you do:*", "When will you arrive in MEXICO City (Date, Approximate Hour)*", "How did you learn about CILAC FREIRE?*"]
	anno=["2017","2018","2019","2020","2021","2022","2023","2024","2025"]
	def salir():#sale de menu buscar
		app.destroy()
		menu(user)
	def listarCSV():
		L=[]
		for i in lista_carpeta("Downloads"):
			if i.find(".crdownload") > -1: os.rename("Downloads/"+i, "Downloads/application_form"+".csv")
		
		for i in lista_carpeta("Downloads"):
			if i.find(".csv") > -1: L.append(i)
		return L
	def revisar(alumno,anio):
		M=crearMatriz(anio)
		reemplzar(M)
		for i in range(len(M)):
			if alumno in M[i]: return True
		return False

	def descargarCSV():
		app2,vp2=crearVentana("Descargando base de datos de www.cilacfreire.mx")
		Label(vp2,text="NO CIERRE LAS VENTANAS",font='arial 20',bg="#FAF3DD").grid(column=1, row=1, sticky=(W,E))
		Label(vp2,text="Este proceso terminará en algunos segundos",font='arial 20',bg="#FAF3DD").grid(column=1, row=2, sticky=(W,E))
		driver=webdriver.Chrome(executable_path=r"C:/Users/CETLALIC/chromedriver.exe")
		driver.get("http://cilacfreire.mx/en/node/6/webform/results/download")
		Label(vp2,text="Inicio de descarga : %s" + str(time.ctime()),font='arial 20',bg="#FAF3DD").grid(column=1, row=3, sticky=(W,E))
		time.sleep(2)
		bt=driver.find_element_by_xpath("//*[@id='edit-submit']")
		bt.click()
		time.sleep(6)
		driver.close()
		Label(vp2,text="Fin de la descarga con exito =) %s" + str(time.ctime()),font='arial 20',bg="#FAF3DD").grid(column=1, row=4, sticky=(W,E))
		time.sleep(2)
		app2.destroy()

	def cargar():
		M=[]
		for i in range(len(listarCSV())):
			A=[]
			temp=[]
			anio=0
			posanio=0
			with open("Downloads"+"/"+listarCSV()[i], newline='',encoding="utf8") as File:
				reader = csv.reader(File)
				for row in reader:
					#print(row)
					A.append(row)
			#reemplzar(A)	
			pos=[]
			#pos=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
			for z in range(len(A[0])):
				if A[0][z] in ing: pos.append(z)
			#if len(pos)!=len(ing): continue
			Label(vp,text="Cargando archivo "+str(i)+":"+listarCSV()[i],font='arial 16 bold',fg="black", bg="#CFF1F7").grid(column=1, row=i, sticky=(W,E))
			for j in range (len(A[0])):
				if A[0][j]=="Created":
					anio=j
					posanio=j
					break
			for j in range(1,len(A)):
				for k in range(0,len(anno)):
					s=A[j][posanio].find(anno[k])
					if s > -1:
						anio=anno[k]
						print("anio: ",anio)
						break
				#archivo=open(anio+"/"+anio+".csv","a")	
				L=[]
				for k in range(len(pos)):
					if (revisar(str(A[j][pos[k]]),anio)==False):
						L.append(str(A[j][pos[k]]))
				M.append(L)
			myData=M
			myFile = open(anio+"/"+anio+".csv", 'w')
			with myFile:
				writer = csv.writer(myFile)
				writer.writerows(myData)
		#darFormatoBD()
		e1=Label(vp,text='Se cargaron con exito los datos =D'+"\n"+"Se respaldo su application Form correctamente"+"\n"+str(i)+" cargados").grid(column=1, row=10, sticky=(W,E))
		Button(vp, text="Cerrar", command=salir).grid(column=1, row=11)
		x=listarCSV()
		for i in range(0,len(listarCSV())):
			print(x[i])
			n=len(glob.glob("respaldos/*.csv"))
			os.rename("Downloads"+"/"+x[i], "application_form"+str(n)+".csv")
			shutil.move("application_form"+str(n)+".csv","respaldos")

	app,vp=crearVentana("Cargar archivo")
	#descargarCSV()
	if len(listarCSV()) > 0:
		cargar()
	else:
		Label(vp,text="No se encuentran aplicaciones disponibles en la carpeta DESCARGAS =(",font='arial 16 bold',fg="black", bg="#CFF1F7").grid(column=1, row=1, sticky=(W,E))
		Button(vp, text="Regresar",font='arial 18',command=salir,bg='#FC933C').grid(column=1, row=2)
	app.mainloop()

def botonActualizar():
	esp=["Nombre", "Nickname", "Genero", "Edad", "Direccion", "CP",	"Ciudad", "Estado", "Pais",	"E-mail", "Programa", "Profesion", "Fecha", "Contacto"]
	A=["2017","2018","2019","2020","2021","2022","2023","2024","2025"]
	L1=["Winter LGBTQ Program","Summer LGBTQ Program","Winter Women and Social Change in Mexico","Summer Women and Social Change in Mexico","Language and Culture for Educators","Medicine in Mexico: Prehispanic, Institutional, Alternative","Spanish Language for Ministry","Regular Program (all year-round)","COSECH","MONSKY","GSU"]
	L=["LGBTQW","LGBTQS","WOMENW","WOMENS","EDUCAT","MEDICI","MINIST","PSR","COSECH","MONSKY","GSU"]
	aniobb=0
	def salir():#sale de menu buscar
		app.destroy()
		menu(1)
	def act():
		alumno=[]
		def salir2():#sale de menu buscar
			app2.destroy()
		app2,vp2=crearVentana("Buscar Alumno")
		for i in range(len(esp)):
			e1=Label(vp2,text=esp[i],font='arial 12 bold',fg="black", bg="#CFF1F7")
			e1.grid(column=1, row=i, sticky=(W,E))
		n=str(entrada1.get())
		c=2
		count=0
		for i in A:
			M=crearMatriz(i)
			#reemplzar(M)
			if len(M)>0:
				for j in range(len(M)):
					esta=False
					for k in range (len(M[j])):
						if M[j][k].find(n) > -1:
							esta=True
					if (esta):
						count+=1
						alumno=M[j]
						aniobb=i
						for l in range(len(M[j])):
							e1=Label(vp2,text=M[j][l],font='arial 12',fg="black", bg="#CFF1F7")
							e1.grid(column=c, row=l, sticky=(W,E))
						c+=1
		Button(vp2, text="Regresar",font='arial 20',command=salir2).grid(column=3, row=100)
		if (count==1):
			def actualizarAlumno():
				app3,vp3=crearVentana("Actualizar"+alumno[0])
				cb=ttk.Combobox(vp3,values=esp,width=10)
				cb.grid(column=1, row=1)
				opcion=""
				def select():
					def actualizarR():
						def actbut():
							def salirs(): app3.destroy()
							M=crearMatriz(aniobb)
							#reemplzar(M)
							M.remove(alumno)
							alumno[indice]=str(entrada1.get())
							M.append(alumno)
							myData=M
							myFile = open(aniobb+"/"+aniobb+".csv", 'w')
							with myFile:
								writer = csv.writer(myFile)
								writer.writerows(myData)
							Label(vp3,text="Se actualizo correctamente el dato: "+str(entrada1.get()),font='arial 16 bold').grid(column=2, row=3, sticky=(W,E))
							Button(vp3, text="Salir",font='arial 20',command=salirs).grid(column=1, row=4)
						v1=""
						Label(vp3,text=esp[indice],font='arial 16 bold').grid(column=1, row=2, sticky=(W,E))
						entrada1=Entry(vp3, width=20, textvariable=v1,font="arial 16")
						entrada1.grid(column=2, row=2)
						Button(vp3, text="Confirme actualizar",font='arial 20',command=actbut).grid(column=1, row=3)
					indice=cb.current()
					Label(vp3,text="¿Desea actualizar? "+esp[indice]+": "+alumno[indice],font='arial 14',fg="black", bg="#CFF1F7").grid(column=3, row=1, sticky=(W,E))
					Button(vp3, text="Actualizar",font='arial 20',command=actualizarR).grid(column=4, row=1)
				Button(vp3, text="Seleccionar",font='arial 20',command=select).grid(column=2, row=1)
			Button(vp2, text="Actualizar",font='arial 20',command=actualizarAlumno).grid(column=1, row=100)
		else:
			e1=Label(vp2,text="¡Siga buscando su alumno!",font='arial 14',fg="black", bg="#CFF1F7")
			e1.grid(column=1, row=100, sticky=(W,E))
		app2.mainloop()
	app,vp=crearVentana("Actualizar Alumno")
	v12=IntVar()
	v12.set(1)
	v13=IntVar()
	v13.set(1)
	v1=""
	e1=Label(vp,text="Ingrese Nombre del alumno a buscar:",font='arial 20 bold',fg="black", bg="#CFF1F7")
	e1.grid(column=1, row=1, sticky=(W,E))
	entrada1=Entry(vp, width=20, textvariable=v1,font='arial 20')
	entrada1.grid(column=1, row=2)
	Button(vp, text="Buscar",font='arial 20',command=act).grid(column=1, row=3)
	Button(vp, text="Regresar",font='arial 20',command=salir).grid(column=1, row=4)
	app.mainloop()

def botonEliminar():
	esp=["Nombre", "Nickname", "Genero", "Edad", "Direccion", "CP",	"Ciudad", "Estado", "Pais",	"E-mail", "Programa", "Profesion", "Fecha", "Contacto"]
	A=["2017","2018","2019","2020","2021","2022","2023","2024","2025"]
	L1=["Winter LGBTQ Program","Summer LGBTQ Program","Winter Women and Social Change in Mexico","Summer Women and Social Change in Mexico","Language and Culture for Educators","Medicine in Mexico: Prehispanic, Institutional, Alternative","Spanish Language for Ministry","Regular Program (all year-round)","COSECH","MONSKY","GSU"]
	L=["LGBTQW","LGBTQS","WOMENW","WOMENS","EDUCAT","MEDICI","MINIST","PSR","COSECH","MONSKY","GSU"]
	aniobb=0
	def salir():#sale de menu buscar
		app.destroy()
		menu(1)
	def act():
		alumno=[]
		def salir2():#sale de menu buscar
			app2.destroy()
		app2,vp2=crearVentana("Buscar Alumno")
		for i in range(len(esp)):
			e1=Label(vp2,text=esp[i],font='arial 12 bold',fg="black", bg="#CFF1F7")
			e1.grid(column=1, row=i, sticky=(W,E))
		n=str(entrada1.get())
		c=2
		count=0
		for i in A:
			M=crearMatriz(i)
			#reemplzar(M)
			if len(M)>0:
				for j in range(len(M)):
					esta=False
					for k in range (len(M[j])):
						if M[j][k].find(n) > -1:
							esta=True
					if (esta):
						count+=1
						alumno=M[j]
						aniobb=i
						for l in range(len(M[j])):
							e1=Label(vp2,text=M[j][l],font='arial 12',fg="black", bg="#CFF1F7")
							e1.grid(column=c, row=l, sticky=(W,E))
						c+=1
		Button(vp2, text="Regresar",font='arial 20',command=salir2).grid(column=3, row=100)
		if (count==1):
			def eliminarAlumno():
				def eliminarA():
					M=crearMatriz(aniobb)
					#reemplzar(M)
					M.remove(alumno)
					myData=M
					myFile = open(aniobb+"/"+aniobb+".csv", 'w')
					with myFile:
						writer = csv.writer(myFile)
						writer.writerows(myData)
						Label(vp2,text="Se Elimino Correcatamente: "+alumno[0],font='arial 14',fg="black", bg="#CFF1F7").grid(column=1, row=104, sticky=(W,E))		
				Label(vp2,text="¿Esta segur@ que desea eliminar a su alumno? "+alumno[0],font='arial 14',fg="black", bg="#CFF1F7").grid(column=1, row=101, sticky=(W,E))
				Button(vp2, text="Sí",font='arial 20',command=eliminarA).grid(column=1, row=102)
				Button(vp2, text="No",font='arial 20',command=salir2).grid(column=2, row=102)
			Button(vp2, text="Eliminar",font='arial 20',command=eliminarAlumno).grid(column=1, row=100)
		else:
			e1=Label(vp2,text="¡Siga buscando su alumno!",font='arial 14',fg="black", bg="#CFF1F7")
			e1.grid(column=1, row=100, sticky=(W,E))
		app2.mainloop()
	app,vp=crearVentana("Actualizar Alumno")
	v12=IntVar()
	v12.set(1)
	v13=IntVar()
	v13.set(1)
	v1=""
	e1=Label(vp,text="Ingrese Nombre del alumno a buscar:",font='arial 20 bold',fg="black", bg="#CFF1F7")
	e1.grid(column=1, row=1, sticky=(W,E))
	entrada1=Entry(vp, width=20, textvariable=v1,font='arial 20')
	entrada1.grid(column=1, row=2)
	Button(vp, text="Buscar",font='arial 20',command=act).grid(column=1, row=3)
	Button(vp, text="Regresar",font='arial 20',command=salir).grid(column=1, row=4)
	app.mainloop()

#darFormatoBD()
time.sleep(1)
menu(1)
#botonCargar(1)
