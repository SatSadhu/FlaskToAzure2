from selenium import webdriver
from time import sleep
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.chrome.options import Options
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pandas as pd


class People_In_Linkedin:

    def __init__(self, nombre_user, contrasena, url_persona_a_buscar):
        self.ember_a_sacar = []
        self.nombre_user = "rodriguezcarlos122@hotmail.com"
        self.contrasena = "hotkatiperri"
        self.url_persona_a_buscar_info = "https://www.linkedin.com/in/tomas-alberti-a46a1820a/"

    def xpath_profile(self, tema):
        sleep(4)
        numero = 1
        num = 0

        sleep(1)
        codigo_fuente = self.driver.page_source
        self.soup = BeautifulSoup(codigo_fuente, 'html.parser')

        patron = r"profilePagedListComponent-(.*)"
        coincidencia = re.search(patron, codigo_fuente)

        self.texto_encontrado = coincidencia.group(0)

        self.all_information = {}

        self.texto_encontrado = self.texto_encontrado.replace(">", "").replace('0"', "").replace('"', "")

        for i in range(100):
            try:
                self.texto_encontrado2 = self.texto_encontrado + f"{i}"

                li_element = self.soup.find('li',
                                            id=f'{self.texto_encontrado2}')
                contenido_li = li_element.get_text()
                contenido_li = contenido_li.replace("\n", "")
                self.contenido = "all_" + tema
                self.all_information[self.contenido] = contenido_li
                print(self.all_information[self.contenido])

                self.intento = self.all_information[self.contenido]
                numero += 1

            except AttributeError:
                continue

    def num_peq_y_num_gran(self):
        # Obtener codigo fuente
        sleep(4)
        codigo_fuente = self.driver.page_source
        self.soup = BeautifulSoup(codigo_fuente, "html.parser")

        matches = re.findall(r'ember(\d+)', codigo_fuente)

        # Saber numero mas chico y numero mas grande de los ember
        if matches:
            # Convertir los números coincidentes a enteros
            self.numeros_ember = [int(match) for match in matches]

    def obtener_cantidad_de_recuadros(self):
        sleep(4)
        self.df_con_todo = pd.DataFrame([])

        sleep(4)
        # Saber cantidad de recuadros
        codigo_fuente = self.driver.page_source
        self.soup = BeautifulSoup(codigo_fuente, 'html.parser')

        self.elementos = self.soup.find_all('section', class_='artdeco-card')

        cantidad_elementos = len(self.elementos)

        elementos2 = self.soup.find_all('section', class_='ad-banner-container')
        cantidad_elementos = cantidad_elementos - len(
            elementos2) - 2  # El -2 son dos que se anaden que son cosas como otros perfiles vistos, etc

        self.df_con_todo["cantidad_de_recuadros"] = cantidad_elementos

    def obtener_titulo_y_ID_de_recuadros(self):
        self.listaa_id = []
        self.listaa_titulo = []
        self.lista_ember = []

        # Obtener el id de los RECUADROS
        for elemento in self.elementos:
            h2_element = elemento.find('h2')
            if h2_element is not None:
                contenido_h2 = h2_element.get_text()
                largo = len(contenido_h2.strip())
                div = largo / 2
                mit = int(largo) - int(div)
                titulos = contenido_h2[:mit + 1]

                # Obtener el valor del atributo "id" del elemento div dentro de la sección actual
                div_element = elemento.find('div', {'id': True})
                if div_element is not None:
                    id_valor = div_element['id']
                    # print(f'Título: {titulos}, ID: {id_valor}')
                    self.listaa_id.append(id_valor)
                    self.listaa_titulo.append(titulos)

        self.df_con_todo["Titulo"] = self.listaa_titulo
        self.df_con_todo["ID"] = self.listaa_id

        for i in self.listaa_id:
            self.obtener_ember_final(titulo=i)

        self.df_con_todo["EMBER"] = self.lista_ember

        for columna in self.df_con_todo.columns:
            self.df_con_todo[columna] = self.df_con_todo[columna].apply(
                lambda x: x.replace("\n", "") if isinstance(x, str) else x)

    def obtener_ember_final(self, titulo):
        gg = self.soup.find_all('section', class_='artdeco-card')
        gg_text = str(gg)
        lineas = gg_text.split('\n')

        # Saber que numero de linea es la del id que conozco yo
        for i, linea in enumerate(lineas):
            linea_con_id = None
            if f'id="{titulo}"' in linea:
                linea_con_id = i
                n_linea_de_ember = linea_con_id - 1
                break

        # Conseguir la linea en donde esta el ember
        for i, linea in enumerate(lineas):
            if i == n_linea_de_ember:
                linea_ember = linea
                match = re.search(r'id="([^"]+)"', linea_ember)
                ember_final = match.group(1)
                self.lista_ember.append(ember_final)

    def comenzar(self):
        try:
            # Configura las opciones de Chrome para el modo silencioso
            chrome_options = Options()
            chrome_options.add_argument("--headless")

            # Crear una instancia del navegador (por ejemplo, Chrome)
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
            except NameError:
                self.driver = webdriver.Chrome()

                # Abrir la página web
            self.driver.get("https://www.linkedin.com")

            # Poner identificaciones
            # Localiza el campo de entrada de texto (username) por su nombre, ID u otro selector
            self.campo_de_texto_user = self.driver.find_element("name", 'session_key')

            # Ingresa texto en el campo de entrada de usuario
            self.campo_de_texto_user.send_keys(self.nombre_user)

            # Localiza el campo de entrada de texto (password) por su nombre, ID u otro selector
            campo_de_texto_psswd = self.driver.find_element("name", 'session_password')

            # Ingresa texto en el campo de entrada de password
            campo_de_texto_psswd.send_keys(self.contrasena)

            # Buscamos boton de iniciar
            boton_iniciar_sesion = self.driver.find_element("xpath",
                                                            '//*[@id="main-content"]/section[1]/div/div/form/div[2]/button')

            # Precionamos boton
            boton_iniciar_sesion.click()

            # Abrir la página web
            sleep(17)

            self.driver.get(self.url_persona_a_buscar_info)

        except Exception as e:
            self.driver.quit()
            People_In_Linkedin.comenzar(self)

    def obtener_informacion(self):
        print("\nBuscando...\n")

        self.num_peq_y_num_gran()

        for i in self.numeros_ember:
            self.ember = f"ember{i}"

            try:
                sleep(0.2)
                self.nombre_completo = self.driver.find_element("xpath",
                                                                f'//*[@id="{self.ember}"]/div[2]/div[2]/div[1]/div[2]')

                if self.ember in self.ember_a_sacar:
                    continue

                print("\nEmber ENCONTRADO!\n")

                self.ember_a_sacar.append(self.ember)
                break

            except NoSuchElementException:
                continue

    def ejecutar(self):
        self.lista_info = []

        nombre_completo = self.soup.find_all(attrs={"id": f"{self.ember}"})

        for elemento in nombre_completo:
            contenido = elemento.get_text()
            self.lista_info.append(contenido)
        for i in self.lista_info:
            self.lista_info = i.replace("\n", "")

        print(self.lista_info)

        # SE LE PUEDE PEDIR A CHATGPT QUE ORDENE EL TEXTO O SIMPLEMENTE HACER UN MODELO PARA ORDENARLO YO (SERIA LO MEJOR)
        # DE ESTA FUNCION TENGO QUE SACAR INFORMACION CONTACTO QUE LO AGARRA COMO TEXTO, Y EN LA FUNCION SIGUIENTE OBTENGO BIEN LA INFO

    def obtener_informacion_contacto(self):
        print("\nBuscando...\n")

        sleep(4)

        # Acceder a la información de contacto para obtener el contacto
        self.informacion_contacto = self.driver.find_element("xpath", '//*[@id="top-card-text-details-contact-info"]')
        self.informacion_contacto.click()

        self.num_peq_y_num_gran()

        for i in self.numeros_ember:
            self.ember = f"ember{i}"

            try:
                sleep(0.2)
                contacto_1 = self.driver.find_element("xpath", f'//*[@id="{self.ember}"]/section/div/section[1]/div/a ')

                if self.ember in self.ember_a_sacar:
                    continue

                print("\nEmber2 ENCONTRADO!\n")
                self.ember_a_sacar.append(self.ember)

                break

            except NoSuchElementException:
                continue

    def ejecutar_informacion_contacto(self):
        self.lista_contactos = []

        contactos = self.soup.find_all(attrs={"id": f"{self.ember}"})

        for elemento in contactos:
            contenido = elemento.get_text()
            self.lista_contactos.append(contenido)
        for i in self.lista_contactos:
            self.lista_contactos = i.replace("\n", "")

        print(self.lista_contactos)

        self.driver.back()

    def obtener_experiencia(self):
        sleep(4)
        try:
            try:
                boton_mostrar_todas_experiencias = self.driver.find_element("xpath",
                                                                            '//*[@id="navigation-index-see-all-experiences"]')
                boton_mostrar_todas_experiencias.click()

                def obtener_informacion_Experiencia_todos_los_PACKS():
                    print("\nBuscando...\n")

                    sleep(5)

                    self.xpath_profile("EXPERIENCE")

                    print("\nEXPERIENCIA ENCONTRADA!\n")

                    self.driver.back()

                obtener_informacion_Experiencia_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_Experiencia_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Experiencia", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        self.experiencia_puesto = self.driver.find_element("xpath",
                                                                           f'//*[@id="{self.ember}"]/div[3]/ul/li[1]/div/div[2]/div[1]/div[1]/div/div/div/div/span[1]')

                    except NoSuchElementException:
                        pass

                def ejecutar_Experiencia_PACKS_CHICOS():
                    self.lista_experiencia_packs_chicos = []

                    experiencia = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in experiencia:
                        contenido = elemento.get_text()
                        self.lista_experiencia_packs_chicos.append(contenido)
                    for i in self.lista_experiencia_packs_chicos:
                        self.lista_experiencia_packs_chicos = i.replace("\n", "")

                    print("\nEXPERIENCIA ENCONTRADA!\n")
                    print(self.lista_experiencia_packs_chicos)

                obtener_informacion_Experiencia_PACKS_CHICOS()
                ejecutar_Experiencia_PACKS_CHICOS()

        except IndexError:
            print("No tiene Experiencia")
            pass

    def obtener_educacion(self):
        try:
            try:
                boton_mostrar_todos_los_estudios = self.driver.find_element("xpath",
                                                                            '//*[@id="navigation-index-see-all-education"]')
                boton_mostrar_todos_los_estudios.click()

                def obtener_informacion_Educacion_todos_los_PACKS():
                    print("\nBuscando...\n")

                    self.xpath_profile("EDUCATION")

                    print("\nEDUCACION ENCONTRADA!\n")

                    self.driver.back()

                obtener_informacion_Educacion_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_EDUCACION_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Educación", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        experiencia_educ = self.driver.find_element("xpath",
                                                                    f'//*[@id="{self.ember}"]/div[3]/ul/li[1]/div/div[2]/div[1]/a/div/div/div/div/span[1]')

                    except NoSuchElementException:
                        pass

                def ejecutar_Educacion_PACKS_CHICOS():
                    self.lista_educacion_packs_chicos = []

                    educacion = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in educacion:
                        contenido = elemento.get_text()
                        self.lista_educacion_packs_chicos.append(contenido)
                    for i in self.lista_educacion_packs_chicos:
                        self.lista_educacion_packs_chicos = i.replace("\n", "")

                    print("\nEDUCACION ENCONTRADA!\n")
                    print(self.lista_educacion_packs_chicos)

                obtener_informacion_EDUCACION_PACKS_CHICOS()
                ejecutar_Educacion_PACKS_CHICOS()

        except IndexError:
            print("No tiene Educacion")
            pass

    def obtener_voluntariados(self):
        try:
            # try:
            # boton_mostrar_todos_los_voluntariados = driver.find_element("xpath", 'BUSCAR COMO ES EL BOTON, PORQUE NO LO SE')
            # boton_mostrar_todos_los_voluntariados.click()

            # def obtener_informacion_Voluntariados_todos_los_PACKS():
            # print("\nBuscando...\n")

            # self.xpath_profile("VOLUNTEERING")

            # print("\nVOLUNTARIADOS ENCONTRADOS!\n")
            # self.driver.back()

            # obtener_informacion_Voluntariados_todos_los_PACKS()

            # except NoSuchElementException:

            def obtener_informacion_VOLUNTARIADOS_PACKS_CHICOS():
                print("\nBuscando...\n")

                pl.obtener_cantidad_de_recuadros()
                pl.obtener_titulo_y_ID_de_recuadros()

                self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Voluntariado", 'EMBER'].values[0]

                try:
                    sleep(0.2)

                    self.voluntariadoss = self.driver.find_element("xpath",
                                                                   f'//*[@id="{self.ember}"]/div[3]/ul/li[1]/div/div[2]/div[1]/div[1]/div/div/div/div/span[1]')

                except NoSuchElementException:
                    pass

            def ejecutar_Voluntariados_PACKS_CHICOS():
                self.lista_voluntariados_packs_chicos = []

                voluntariados = self.soup.find_all(attrs={"id": f"{self.ember}"})

                for elemento in voluntariados:
                    contenido = elemento.get_text()
                    self.lista_voluntariados_packs_chicos.append(contenido)
                for i in self.lista_voluntariados_packs_chicos:
                    self.lista_voluntariados_packs_chicos = i.replace("\n", "")

                print("\nVOLUNTARIADOS ENCONTRADOS!\n")
                print(self.lista_voluntariados_packs_chicos)

            obtener_informacion_VOLUNTARIADOS_PACKS_CHICOS()
            ejecutar_Voluntariados_PACKS_CHICOS()

        except IndexError:
            print("No tiene Voluntariados")
            pass

    def obtener_licencias_y_certificaciones(self):
        try:
            try:
                boton_mostrar_todas_las_lic_y_cert = self.driver.find_element("xpath",
                                                                              '//*[@id="navigation-index-see-all-licenses-and-certifications"]')
                boton_mostrar_todas_las_lic_y_cert.click()

                def obtener_informacion_lic_y_cert_todos_los_PACKS():
                    print("\nBuscando...\n")

                    self.xpath_profile("LICENSES-AND-CERTIFICATIONS")

                    print("\nLICENCIAS Y CERTIFICACIONES ENCONTRADAS!\n")

                    self.driver.back()

                obtener_informacion_lic_y_cert_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_LIC_Y_CERT_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = \
                    self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Licencias y certificaciones", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        self.licencias_y_certificaciones = self.driver.find_element("xpath",
                                                                                    f'//*[@id="{self.ember}"]/div[3]/ul/li[1]/div/div[2]/div/div[1]/div/div/div/div/span[1]')

                    except NoSuchElementException:
                        pass

                def ejecutar_Lic_y_cert_PACKS_CHICOS():
                    self.lista_lic_y_cert_packs_chicos = []

                    lic_y_cert = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in lic_y_cert:
                        contenido = elemento.get_text()
                        self.lista_lic_y_cert_packs_chicos.append(contenido)
                    for i in self.lista_lic_y_cert_packs_chicos:
                        self.lista_lic_y_cert_packs_chicos = i.replace("\n", "")

                    print("\nLICENCIAS Y CERTIFICACIONES ENCONTRADAS!\n")
                    print(self.lista_lic_y_cert_packs_chicos)

                obtener_informacion_LIC_Y_CERT_PACKS_CHICOS()
                ejecutar_Lic_y_cert_PACKS_CHICOS()

        except IndexError:
            print("No tiene Licencias y Certificaciones")
            pass

    def obtener_proyectos(self):
        try:
            try:
                boton_mostrar_todos_los_proyectos = self.driver.find_element("xpath",
                                                                             '//*[@id="navigation-index-see-all-projects"]')
                boton_mostrar_todos_los_proyectos.click()

                def obtener_informacion_Proyectos_todos_los_PACKS():
                    print("\nBuscando...\n")

                    self.xpath_profile("PROJETS")

                    print("\nPROYECTOS ENCONTRADOS!\n")
                    self.driver.back()

                obtener_informacion_Proyectos_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_PROYECTOS_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Proyectos", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        self.proyectos = self.driver.find_element("xpath",
                                                                  f'//*[@id="{self.ember}"]/div[3]/ul/li[1]/div/div[2]/div[1]/div[1]/div/div/div/div/span[1]')
                    except NoSuchElementException:
                        pass

                def ejecutar_Proyectos_PACKS_CHICOS():
                    self.lista_proyectos_packs_chicos = []

                    proyectos = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in proyectos:
                        contenido = elemento.get_text()
                        self.lista_proyectos_packs_chicos.append(contenido)
                    for i in self.lista_proyectos_packs_chicos:
                        self.lista_proyectos_packs_chicos = i.replace("\n", "")

                    print("\nPROYECTOS ENCONTRADOS!\n")
                    print(self.lista_proyectos_packs_chicos)

                obtener_informacion_PROYECTOS_PACKS_CHICOS()
                ejecutar_Proyectos_PACKS_CHICOS()

        except IndexError:
            print("No tiene Proyectos")
            pass

    def obtener_datos_destacados(self):
        try:
            def obtener_informacion_datos_destacados():
                print("\nBuscando...\n")

                pl.obtener_cantidad_de_recuadros()
                pl.obtener_titulo_y_ID_de_recuadros()

                self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Datos destacados", 'EMBER'].values[0]

                try:
                    sleep(0.2)
                    self.datos_destacados = self.driver.find_element("xpath",
                                                                     f'//*[@id="{self.ember}"]/div[3]/ul/li/div/div[2]/div/div[1]/div/div/div/div/span[1]')

                except NoSuchElementException:
                    pass

            def ejecutar_datos_destacados():
                self.lista_datos_destacados = []

                datos_destacados = self.soup.find_all(attrs={"id": f"{self.ember}"})

                for elemento in datos_destacados:
                    contenido = elemento.get_text()
                    self.lista_datos_destacados.append(contenido)
                for i in self.lista_datos_destacados:
                    self.lista_datos_destacados = i.replace("\n", "")

                print("\nDatos Destacados ENCONTRADOS!\n")
                print(self.lista_datos_destacados)

            obtener_informacion_datos_destacados()
            ejecutar_datos_destacados()

        except IndexError:
            print("No tiene Datos Destacados")
            pass

    def obtener_primeras_3_actividades(self):
        try:
            def obtener_actividad():
                print("\nBuscando...\n")

                pl.obtener_cantidad_de_recuadros()
                pl.obtener_titulo_y_ID_de_recuadros()

                self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Actividad", 'EMBER'].values[0]

                try:
                    sleep(0.2)
                    self.actividades = self.driver.find_element("xpath",
                                                                f'//*[@id="{self.ember}"]/div[3]/ul/li/div/div[2]/div/div[1]/div/div/div/div/span[1]')

                except NoSuchElementException:
                    pass

            def ejecutar_actividades():
                self.lista_actividades = []

                actividades = self.soup.find_all(attrs={"id": f"{self.ember}"})

                for elemento in actividades:
                    contenido = elemento.get_text()
                    self.lista_actividades.append(contenido)
                for i in self.lista_actividades:
                    self.lista_actividades = i.replace("\n", "")

                print("\nACTIVIDADES ENCONTRADAS!\n")
                print(self.lista_actividades)

            obtener_actividad()
            ejecutar_actividades()

        except IndexError:
            print("No tiene Actividades")
            pass

    def obtener_acerca_de(self):
        try:
            def obtener_informacion_acerca_de():
                print("\nBuscando...\n")

                pl.obtener_cantidad_de_recuadros()
                pl.obtener_titulo_y_ID_de_recuadros()

                self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Acerca de", 'EMBER'].values[0]

                try:
                    sleep(0.2)
                    self.acerca_de = self.driver.find_element("xpath",
                                                              f'//*[@id="{self.ember}"]/div[2]/div/div/div/h2/span[1]')

                except NoSuchElementException:
                    pass

            def ejecutar_acerca_de():
                self.lista_acerca_de = []

                acerca_de = self.soup.find_all(attrs={"id": f"{self.ember}"})

                for elemento in acerca_de:
                    contenido = elemento.get_text()
                    self.lista_acerca_de.append(contenido)
                for i in self.lista_acerca_de:
                    self.lista_acerca_de = i.replace("\n", "")

                print("\nACERCA DE ENCONTRADO!!\n")
                print(self.lista_acerca_de)

            obtener_informacion_acerca_de()
            ejecutar_acerca_de()

        except IndexError:
            print("No tiene Acerca_De")
            pass

    def obtener_conocimientos_y_aptitudes(self):
        try:
            try:
                sleep(3)
                boton_mostrar_todos_los_conocimientos_y_aptitudes = self.driver.find_element("xpath",
                                                                                             '//*[@id="navigation-index-Mostrar-todas-las-aptitudes-50-"]')
                boton_mostrar_todos_los_conocimientos_y_aptitudes.click()

                for i in range(4):
                    sleep(2)
                    scroll_amount = 5000
                    self.driver.execute_script(f'window.scrollBy(0, {scroll_amount});')

                def obtener_info_conocimientos_y_aptitudes_todos_los_PACKS():
                    print("\nBuscando...\n")

                    self.xpath_profile(tema="SKILLS")

                    print("\nCONOCIMIENTOS Y APTITUDES ENCONTRADAS!\n")

                    self.driver.back()

                obtener_info_conocimientos_y_aptitudes_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_conocimientos_y_aptitudes_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = \
                    self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Conocimientos y aptitudes", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        self.conocimientos_y_aptitudes = self.driver.find_element("xpath",
                                                                                  f'//*[@id="{self.ember}"]/div[3]/ul/li[1]/div/div[2]/div[1]/a/div/div/div/div/span[1]')

                    except NoSuchElementException:
                        pass

                def ejecutar_conocimientos_y_aptitudes_PACKS_CHICOS():
                    self.lista_conocimientos_y_aptitudes_packs_chicos = []

                    conocimientos_y_aptitudes = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in conocimientos_y_aptitudes:
                        contenido = elemento.get_text()
                        self.lista_conocimientos_y_aptitudes_packs_chicos.append(contenido)
                    for i in self.lista_conocimientos_y_aptitudes_packs_chicos:
                        self.lista_conocimientos_y_aptitudes_packs_chicos = i.replace("\n", "")

                    print("\nCONOCIMIENTOS Y APTITUDES ENCONTRADOS!\n")
                    print(self.lista_conocimientos_y_aptitudes_packs_chicos)

                obtener_informacion_conocimientos_y_aptitudes_PACKS_CHICOS()
                ejecutar_conocimientos_y_aptitudes_PACKS_CHICOS()

        except IndexError:
            print("No tiene Conocimientos y Aptitudes")
            pass

    def obtener_idiomas(self):
        try:
            def obtener_informacion_idiomas():
                print("\nBuscando...\n")

                pl.obtener_cantidad_de_recuadros()
                pl.obtener_titulo_y_ID_de_recuadros()

                self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Idiomas", 'EMBER'].values[0]

                try:
                    sleep(0.2)
                    self.idiomas = self.driver.find_element("xpath",
                                                            f'//*[@id="{self.ember}"]/div[2]/div/div/div/h2/span[1]')

                except NoSuchElementException:
                    pass

            def ejecutar_idiomas():
                self.lista_idiomas = []

                idiomas = self.soup.find_all(attrs={"id": f"{self.ember}"})

                for elemento in idiomas:
                    contenido = elemento.get_text()
                    self.lista_idiomas.append(contenido)
                for i in self.lista_idiomas:
                    self.lista_idiomas = i.replace("\n", "")

                print("\IDIOMAS ENCONTRADOS!!\n")
                print(self.lista_idiomas)

            obtener_informacion_idiomas()
            ejecutar_idiomas()

        except IndexError:
            print("No tiene Idiomas")
            pass

    def obtener_causas_beneficas(self):
        try:
            def obtener_informacion_causas_beneficas():
                print("\nBuscando...\n")

                pl.obtener_cantidad_de_recuadros()
                pl.obtener_titulo_y_ID_de_recuadros()

                self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Causas benéficas", 'EMBER'].values[0]

                try:
                    sleep(0.2)
                    self.causas_beneficas = self.driver.find_element("xpath",
                                                                     f'//*[@id="{self.ember}"]/div[2]/div/div/div/h2/span[1]')

                except NoSuchElementException:
                    pass

            def ejecutar_causas_beneficas():
                self.lista_causas_beneficas = []

                causas_beneficas = self.soup.find_all(attrs={"id": f"{self.ember}"})

                for elemento in causas_beneficas:
                    contenido = elemento.get_text()
                    self.lista_causas_beneficas.append(contenido)
                for i in self.lista_causas_beneficas:
                    self.lista_causas_beneficas = i.replace("\n", "")

                print("\CAUSAS BENEFICAS ENCONTRADOS!!\n")
                print(self.lista_causas_beneficas)

            obtener_informacion_causas_beneficas()
            ejecutar_causas_beneficas()

        except IndexError:
            print("No tiene Causas Beneficas")
            pass

    def obtener_reconocimientos_y_premios(self):
        try:
            try:
                boton_mostrar_todos_los_reconocimientos_y_premios = self.driver.find_element("xpath",
                                                                                             '//*[@id="navigation-index-see-all-honorsandawards"]')
                boton_mostrar_todos_los_reconocimientos_y_premios.click()

                def obtener_informacion_reconocimientos_y_premios_todos_los_PACKS():
                    sleep(1)

                    print("\nBuscando...\n")

                    self.xpath_profile("HONORS_AND_AWARDS")

                    print("\nRECONOCIMIENTOS Y PREMIOS ENCONTRADOS!\n")

                    self.driver.back()

                obtener_informacion_reconocimientos_y_premios_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_RECONOCIMIENTOS_Y_PREMIOS_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = \
                    self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Reconocimientos Y premios", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        self.reconocimientos_y_premios = self.driver.find_element("xpath",
                                                                                  f'//*[@id="{self.ember}"]/div[2]/div/div/div/h2/span[1]')

                    except NoSuchElementException:
                        pass

                def ejecutar_reconocimientos_y_premios_PACKS_CHICOS():
                    self.lista_reconocimientos_y_premios_packs_chicos = []

                    reconocimientos_y_premios = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in reconocimientos_y_premios:
                        contenido = elemento.get_text()
                        self.lista_reconocimientos_y_premios_packs_chicos.append(contenido)
                    for i in self.lista_reconocimientos_y_premios_packs_chicos:
                        self.lista_reconocimientos_y_premios_packs_chicos = i.replace("\n", "")

                    print("\nRECONOCIMIENTOS Y PREMIOS ENCONTRADOS!\n")
                    print(self.lista_reconocimientos_y_premios_packs_chicos)

                obtener_informacion_RECONOCIMIENTOS_Y_PREMIOS_PACKS_CHICOS()
                ejecutar_reconocimientos_y_premios_PACKS_CHICOS()

        except IndexError:
            print("No tiene Reconocimientos y Premios")
            pass

    def obtener_publicaciones(self):
        try:
            try:
                boton_mostrar_todas_las_publicaciones = self.driver.find_element("xpath",
                                                                                 '//*[@id="navigation-index-see-all-publication"]')
                boton_mostrar_todas_las_publicaciones.click()

                def obtener_informacion_publicaciones_todos_los_PACKS():
                    sleep(1)

                    print("\nBuscando...\n")

                    self.xpath_profile("PUBLICATIONS")

                    print("\nPUBLICACIONES ENCONTRADAS!\n")

                    self.driver.back()

                obtener_informacion_publicaciones_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_PUBLICACIONES_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Publicaciones", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        self.publicaciones = self.driver.find_element("xpath",
                                                                      f'//*[@id="{self.ember}"]/div[2]/div/div/div/h2/span[1]')

                    except NoSuchElementException:
                        pass

                def ejecutar_publicaciones_PACKS_CHICOS():
                    self.lista_publicaciones_packs_chicos = []

                    publicaciones = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in publicaciones:
                        contenido = elemento.get_text()
                        self.lista_publicaciones_packs_chicos.append(contenido)
                    for i in self.lista_publicaciones_packs_chicos:
                        self.lista_publicaciones_packs_chicos = i.replace("\n", "")

                    print("\nPUBLICACIONES ENCONTRADAS!\n")
                    print(self.lista_publicaciones_packs_chicos)

                obtener_informacion_PUBLICACIONES_PACKS_CHICOS()
                ejecutar_publicaciones_PACKS_CHICOS()

        except IndexError:
            print("No tiene Publicaciones")
            pass

    def obtener_organizaciones(self):
        try:
            try:
                boton_mostrar_todas_las_organizaciones = self.driver.find_element("xpath",
                                                                                  '//*[@id="navigation-index-see-all-organizations"]')
                boton_mostrar_todas_las_organizaciones.click()

                def obtener_informacion_organizaciones_todos_los_PACKS():
                    sleep(1)

                    print("\nBuscando...\n")

                    self.xpath_profile("ORGANIZATIONS")

                    print("\nORGANIZACIONES ENCONTRADAS!\n")

                    self.driver.back()

                obtener_informacion_organizaciones_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_ORGANIZACIONES_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Organizaciones", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        self.organizaciones = self.driver.find_element("xpath",
                                                                       f'//*[@id="{self.ember}"]/div[2]/div/div/div/h2/span[1]')

                    except NoSuchElementException:
                        pass

                def ejecutar_organizaciones_PACKS_CHICOS():
                    self.lista_organizaciones_packs_chicos = []

                    organizaciones = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in organizaciones:
                        contenido = elemento.get_text()
                        self.lista_organizaciones_packs_chicos.append(contenido)
                    for i in self.lista_organizaciones_packs_chicos:
                        self.lista_organizaciones_packs_chicos = i.replace("\n", "")

                    print("\nORGANIZACIONES ENCONTRADAS!\n")
                    print(self.lista_organizaciones_packs_chicos)

                obtener_informacion_ORGANIZACIONES_PACKS_CHICOS()
                ejecutar_organizaciones_PACKS_CHICOS()

        except IndexError:
            print("No tiene Organizaciones")
            pass

    def obtener_cursos(self):
        try:
            try:
                boton_mostrar_todos_los_cursos = self.driver.find_element("xpath",
                                                                          '//*[@id="navigation-index-see-all-courses"]')
                boton_mostrar_todos_los_cursos.click()

                def obtener_informacion_cursos_todos_los_PACKS():
                    sleep(1)

                    print("\nBuscando...\n")

                    self.xpath_profile("COURSES")

                    print("\nCURSOS ENCONTRADOS!\n")

                    self.driver.back()

                obtener_informacion_cursos_todos_los_PACKS()

            except NoSuchElementException:

                def obtener_informacion_CURSOS_PACKS_CHICOS():
                    print("\nBuscando...\n")

                    pl.obtener_cantidad_de_recuadros()
                    pl.obtener_titulo_y_ID_de_recuadros()

                    self.ember = self.df_con_todo.loc[self.df_con_todo['Titulo'] == "Cursos", 'EMBER'].values[0]

                    try:
                        sleep(0.2)
                        self.cursos = self.driver.find_element("xpath",
                                                               f'//*[@id="{self.ember}"]/div[2]/div/div/div/h2/span[1]')

                    except NoSuchElementException:
                        pass

                def ejecutar_cursos_PACKS_CHICOS():
                    self.lista_cursos_packs_chicos = []

                    cursos = self.soup.find_all(attrs={"id": f"{self.ember}"})

                    for elemento in cursos:
                        contenido = elemento.get_text()
                        self.lista_cursos_packs_chicos.append(contenido)
                    for i in self.lista_cursos_packs_chicos:
                        self.lista_cursos_packs_chicos = i.replace("\n", "")

                    print("\nCURSOS ENCONTRADAS!\n")
                    print(self.lista_cursos_packs_chicos)

                obtener_informacion_CURSOS_PACKS_CHICOS()
                ejecutar_cursos_PACKS_CHICOS()

        except IndexError:
            print("No tiene Cursos")
            pass

    def ver_df_con_todo(self):
        print(self.df_con_todo)


pl = People_In_Linkedin()
pl.comenzar()
pl.obtener_informacion()
pl.ejecutar()
pl.obtener_informacion_contacto()
pl.ejecutar_informacion_contacto()
pl.obtener_experiencia()
pl.obtener_educacion()
pl.obtener_voluntariados()
pl.obtener_licencias_y_certificaciones()
pl.obtener_proyectos()
pl.obtener_datos_destacados()
pl.obtener_primeras_3_actividades()
pl.obtener_acerca_de()
pl.obtener_conocimientos_y_aptitudes()
pl.obtener_idiomas()
pl.obtener_causas_beneficas()
pl.obtener_reconocimientos_y_premios()
pl.obtener_publicaciones()
pl.obtener_organizaciones()
pl.obtener_cursos()
pl.ver_df_con_todo()
# Falta PATENTES
# Falta CALIFICACIONES DE PRUEBAS
# Capaz RECOMENDACIONES
# Capaz ELEMENTO DESTACADO