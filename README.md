# Sistema de recomendación de políticas de tráfico BGP

Resumen
============
Las tecnologías de la información y comunicación son áreas de investigación en constante crecimiento. Los numerosos avances del sector proporcionan herramientas para acceder a una gran variedad de información y servicios desde cualquier parte del mundo. Estas herramientas se podrían resumir en una única palabra, Internet.

Internet es una herramienta de carácter global cuyo funcionamiento es posible gracias a complejos mecanismos y protocolos desarrollados a lo largo de la historia. Cada uno de estos mecanismos se encarga de gestionar una característica concreta, siendo BGP (*Border Gateway Protocol*) uno de los protocolos más relevantes sobre los que se sostiene Internet. Sin embargo, este protocolo que se encarga del intercambio de información de encaminamiento global, es gestionado y configurado de manera local por los diferentes ISP (*Internet Service Provider*), empresas tecnológicas, universidades, agencias gubernamentales e instituciones científicas. Esto hace que los intereses particulares de algunas entidades intervengan en el encaminamiento del tráfico de red, causando en ocasiones ciertos problemas.

En este trabajo se presenta un estudio acerca de los diferentes problemas que alberga este protocolo, proporcionando un medio para observar los eventos que se producen y recomendando posibles configuraciones con el fin de evitar interrupciones de servicio inesperadas o el secuestro indeseado de prefijos.

**Palabras clave**
   
BGP (*Border Gateway Protocol*), AS (*Autonomous System*), *Outages*, *Hijacks*, BGPMon, BGPStream

Puesta en marcha de la aplicación
=================================
Dentro de este proyecto se encuentra la carpeta denominada
`/dependencies_installation_dir` que contiene el archivo
`requirements.txt` con la información de las dependencias necesarias.

BgpRS actualmente solo esta preparado para funcionar en distribuciones de Linux, se debe
proceder a crear un entorno virtual de Python3 para instalar las citadas
dependencias. Esto ultimo se puede realizar mediante los pasos
enumerados a continuación.

1.  **Creación del entorno virtual:**

    `python3 -m venv venv`

2.  **Activación del entrono virtual:**

    `source venv/bin/activate`

3.  **Instalación de dependencias del proyecto:**

    `pip install -r dependencies_installation_dir/requirements.txt`

De todas las dependencias que se instalaran, podría decirse que las mas
relevantes son las librerías de TweePy [@tweepy] y Pydrive [@pydrive].
Es importante destacar que estas dos librerías necesitan de permisos y
la asignación de credenciales para cumplir con su cometido, siendo
necesaria su especificación en el código de la aplicación. En
consecuencia de esto, se proporciona este capitulo con el fin de conocer
características a más bajo nivel de la aplicación y mostrar cómo dar
funcionamiento a la aplicación.

Twitter API
-----------

Como se repetido en múltiples ocasiones, las información obtenida a
través de la API de Twitter tiene enorme relevancia para BgpRS. Sin
embargo, para que la aplicación pueda utilizar las funcionalidades de
esta API, es necesario seguir ciertas directrices que se detallan a
continuación.

En primer lugar, es necesario puntualizar que BgpRS utiliza funciones de
esta API que solo están disponibles con los permisos que otorga el plan
*Academic Research* de Twitter, la necesidad de esto se ha podido ver en
detalle en la sección
[\[sec:problemasObInfo\]](#sec:problemasObInfo){reference-type="ref"
reference="sec:problemasObInfo"} de esta memoria. Por ello, el primer
paso necesario para poner en marcha la aplicación será solicitar acceso
a al plan mencionado.

Para poder realizar la solicitud correspondiente, primero se debe tener
una cuenta de Twitter para realizar el registro en la plataforma
*developer* [^1] de esta entidad. Este proceso de solicitud es bastante
intuitivo. Sin embargo, como el acceso a este plan esta restringido para
ciertos usuarios, se requiere del consentimiento de Twitter, por lo que
será necesario el intercambio de cierta cantidad de *e-mails*.

Una ver realizado todo esto, sera posible crear un proyecto con el fin
de poder dar acceso a los servicios a la aplicación BgpRS. Si todo el
proceso se ha realizado correctamente, el nuevo perfil de *Twitter
Developer* se asemejará al representado en la siguiente figura.

![Permisos *Academic Research* en Twitter, *fuente:
<https://developer.twitter.com/en/portal/products>*[]{label="fig:twitDevACC"}](IMG/CAP7/academic_research_plan.PNG)
### Asignación de credenciales dentro de BgpRS

Una vez obtenido el acceso al plan *Academic Research*, será posible
obtener las credenciales necesarias para que TweePy [@tweepy] pueda
ejecutar las solicitudes de BgpRS. El acceso a estas credenciales y su
lectura se puede realizar a través del portal *developer* de Twitter tal
y como se representa en la siguiente figura.

![Acceso a credenciales de Twitter, *fuente:
<https://developer.twitter.com/en/portal/projects/1495420932801785863/apps/23448073/keys>*[]{label="fig:twitDevACC"}](IMG/CAP7/Credenciales_Twitter_web.PNG)

Con estas credenciales en nuestra posesión, ya solo se necesita
especificar su valor dentro del código de BgpRS. Esto se debe realizar
mediante la modificación del archivo `twitterDevCredentials.py` situado
en la carpeta `/API_classes`, asignando valor a cada una de las
variables mostradas en la siguiente figura.

![Archivo en BgpRS para introducir las credenciales de
Twitter[]{label="fig:twitDevACC"}](IMG/CAP7/Credenciales_Twitter.PNG)

Una vez realizados todos estos pasos, la aplicación será capaz de
obtener y actualizar la información de eventos BGP identificados por
Cisco. Sin embargo, para proceder a su almacenamiento, se necesita
realizar proceso similar para la librería de PyDrive [@pydrive], el cual
se detalla en la siguiente sección.

Google API
----------

Para poder ejecutar BgpRS sin errores, es fundamental seguir los pasos
que se describen en esta sección, en esta, se podrá observar cuales son
los requerimientos para que la aplicación se pueda conectar a los
servicios de Google Drive. Para poder obtener las credenciales
necesarias para la aplicación, es necesario poseer en una cuenta de
Gmail y acceder a la consola de *Google Cloud Platform* [^2]. A través
de esta consola, se podrá crear un proyecto para posteriormente activar
el servicio correspondiente de Google Drive.

![Credenciales de Google Drive, *fuente:
<https://console.cloud.google.com/apis/credentials?authuser=1&project=phrasal-clover-312717>*[]{label="fig:credenGdriveP1"}](IMG/CAP7/Credenciales_gdrive.png)

En la figura anterior se representa el proceso para crear y
obtener las credenciales necesarias para hacer uso de las
funcionalidades de PyDrive [@pydrive]. En primer lugar, se deberá
ingresar en el menú de `API y servicios`, y dentro de este, en el
apartado de `Credenciales` para crear unas del tipo
`ID de cliente de OAuth`. Para completar el proceso se deberán rellenar
los campos solicitados, si todo se realiza de la manera correcta, se
podrá acceder a las credenciales, que en el caso ilustrado son las
denominadas como `bgp_stream`.

Siguiendo la misma imagen, si se navega a través del frontal de la
consola, se encontrará el botón de descarga resaltado en verde (3). Si
presionamos este botón, se desplegará una pestaña como la resaltada en
color morado (4) y se podrán obtener las credenciales que necesita
BgpRS.

Dentro del proyecto de BgpRs, se deberá crear un archivo de extensión
`.yaml`, que deberá denominarse `settings.yaml` y deberá situarse en la
raíz siguiendo la imagen
[\[fig:OrgDirectorios\]](#fig:OrgDirectorios){reference-type="ref"
reference="fig:OrgDirectorios"}. Este archivo, servirá para indicar las
credenciales de Google Drive a la aplicación BgpRS, por lo que deberá
poseer la información representada en la imagen
[\[fig:credenGdriveYaml\]](#fig:credenGdriveYaml){reference-type="ref"
reference="fig:credenGdriveYaml"}.

En el archivo `settings.yaml`, se deberá dar valor a los campos
`client_secret` y `client_id` con la información de las credenciales de
Google Drive [^3]. Una vez configurado este archivo, cuando ejecutemos
la aplicación por primera vez, se abrirá una pestaña en el navegador
pidiendo la confirmación de permisos de usuario. Si aceptan dichos
permisos, se generaran automáticamente los archivos `credentials.json` y
`client_secrets.json` con la información necesaria para no tener que
realizar esta acción en las próximas ejecuciones.

### Asignación de identificadores de carpeta dentro de BgpRS

Con los pasos realizados anteriormente, ya solo es necesario crear una
carpeta de Drive donde BgpRS almacenará y obtendrá la diferente
información. Esta carpeta, deberá estar organizada de manera similar a
la representada en la siguiente figura. El nombre de estas carpetas no tiene
porque ser idéntico, ya que de estas, como se vera mas adelante, solo se
utilizará el identificador de las mismas.

![Distribución de carpetas en Google Drive, *fuente:
<https://drive.google.com/drive/u/1/folders/1dwxWQoyJvVZeOto3X0QjDy3VhQ6jhmuL>*[]{label="fig:distribuGdrive"}](IMG/CAP7/Distribu_gdrive.PNG)

El contenido de estas carpetas tiene diferente significado para BgpRS.
Por un lado, la carpeta `/Scrapped_From_Twitter` contendrá el archivo
donde se guardaran y actualizaran los datos obtenidos de Twitter. Este
archivo sera utilizado por la aplicación para clasificar la información,
generando como resultado un archivo analizable para la misma que será
almacenado en la carpeta `/Classified_By_BgpRS`.

Por ultimo, la aplicación incorpora funcionalidades aumentar estos datos
de manera estático, para realizar esto, la aplicación obtendrá la
información del archivo almacenado en la carpeta `/Classified_By_BgpRS`
y la actualizará con los nuevos datos. Después de realizar todo esto, se
generará un nuevo archivo que se almacenará en la carpeta
`/Posible_Extended_Data`.

Una vez creadas las tres carpetas, se deberán obtener sus
identificadores, ya que como se ha mencionado, la aplicación necesitara
conocer su valor. Esta información se puede extraer del mismo navegador,
ya que en la ultima parte de la *url* de cada una de estas carpetas se
encuentra su identificador. El proceso de obtención de estos
identificadores se puede observar en la figura
[1.6](#fig:folderids).

![Obtención de identificadores de carpeta, *fuente:
<https://drive.google.com/drive/u/1/folders/1pV892qsDAl28h7ivBVX3PqiMeF1oQmNK>*[]{label="fig:folderids"}](IMG/CAP7/Folder_ids_gdrive.PNG)[1.6](fig:folderids)

Una vez obtenidos cada uno de los identificadores, solo hace falta
indicarlos en la parte correspondiente del código de BgpRS. Esta
asignación, debe realizarse en el archivo `Data_classifier_class.py` que
se encuentra situado dentro de la carpeta `/API_classes`. Según esto
ultimo, el valor de estos identificadores de carpeta se deberá indicar
sobre las variables que se resaltan en rojo en la figura
[1.7](#fig:IDSBGPRSGDRIVE){reference-type="ref"
reference="fig:IDSBGPRSGDRIVE"}.

![Asignación de identificadores de carpeta en
BgpRS[]{label="fig:IDSBGPRSGDRIVE"}](IMG/CAP7/Carpetas_gDrive_bgpRS.PNG){#fig:IDSBGPRSGDRIVE
width="60%"}

Con cada uno de estos pasos realizados, BgpRS estará capacitado para
almacenar y obtener la información necesaria para su funcionamiento,
proporcionando la posibilidad de obtener, actualizar y analizar los
datos al usuario a través su interfaz gráfica.

Interfaz gráfica
----------------

En los capítulos
[\[cap:asnPaises\]](#cap:asnPaises){reference-type="ref"
reference="cap:asnPaises"} y
[\[cap:sistemasRecomendacionBGP\]](#cap:sistemasRecomendacionBGP){reference-type="ref"
reference="cap:sistemasRecomendacionBGP"} se han podido observar las
funcionalidades principales de BgpRS. Sin embargo, existen otras
funcionalidades adicionales que el usuario puede realizar a través de la
interfaz gráfica.

A lo largo de este capitulo, se han explicado cada uno de los aspectos
necesarios para que la aplicación pudiese utilizar las funcionalidades
de obtención y almacenamiento de la información. Para que el usuario
pudiese ejecutar estas funcionalidades de manera sencilla, se decidió
implementar los accesos rápidos de la interfaz que se observan en la
figura [1.8](#fig:accesorapid){reference-type="ref"
reference="fig:accesorapid"}. La descripción de cada uno de estos
botones se realizará en las secciones a continuación.

![Funcionalidades adicionales de
BgpRS[]{label="fig:accesorapid"}](IMG/CAP7/iface_bgp_datos.png){#fig:accesorapid
width="100%"}

### Actualización de datos vía Twitter

Una de las posibilidades que se le proporcionan al usuario es la
posibilidad de obtener y actualizar los datos a través de la API de
Twitter. Este proceso esta automatizado, de tal forma que si el usuario
no posee datos en las carpetas de su Google Drive, obtendrá los 3500
*tweets* mas recientes del usuario *\@bgpstream* y los clasificara para
la aplicación, generando los archivos correspondientes en las carpetas
`/Scrapped_From_Twitter` y `/Classified_By_BgpRS` mencionadas
anteriormente.

Si por el contrario, el usuario ya posee datos en estas carpetas, la
aplicación se encargara de actualizarlos. En este aspecto, cabe destacar
que la aplicación puede tardar varios minutos, ya que depende de la
cantidad de datos que se obtengan. Además, como en ocasiones el comando
`whois` puede no haber obtenido el país de cada uno de los eventos BGP,
con el fin de mejorar la calidad de datos, se decidió que la aplicación
reclasificara los datos que ya poseyese, ralentizando este proceso en
gran medida.

Por esta razón, para que el usuario no estuviese esperando
infinitamente, se decidió implementar un hilo de proceso independiente
para realizar este tipo de acciones, por lo que el usuario podrá
examinar los datos ya clasificados mientras espera.El proceso de
ejecución de este botón desde el punto de vista del usuario se puede ver
reflejado en la figura [1.9](#fig:ejecucionUPDATE){reference-type="ref"
reference="fig:ejecucionUPDATE"}.

![Acción del proceso de actualizado de
datos.[]{label="fig:ejecucionUPDATE"}](IMG/CAP7/Ejecuta_update.PNG){#fig:ejecucionUPDATE
width="80%"}

Como se puede observar, en primer lugar se le preguntará al usuario si
realmente quiere actualizar los datos. Después de que el usuario de
confirmación, el proceso de actualizado comenzará y al finalizar
notificará al usuario a través del mensaje reflejado en la figura
[1.10](#fig:dataupdated){reference-type="ref"
reference="fig:dataupdated"}.

![Mensaje de notificación sobre el actualizado de
datos[]{label="fig:dataupdated"}](IMG/CAP7/data_updated_msg.png){#fig:dataupdated
width="30%"}

### Datos sintéticos

En la sección
[\[secc:CreadatosEstaticos\]](#secc:CreadatosEstaticos){reference-type="ref"
reference="secc:CreadatosEstaticos"} se ha explicado detalladamente como
construir un archivo de datos para la alimentación estática de la
aplicación, el cual debe seguir cierta sintaxis. El botón de la
interfaz, `Load static file`, permite al usuario seleccionar un archivo
local, que mantenga dicha sintaxis, para incorporar los datos a BgpRS.

La ejecución de esta funcionalidad, se hace a través de un hilo
independiente de la misma manera que para el actualizado de datos de
Twitter. Después que el usuario pulse sobre el botón de
`Load static file`, la aplicación desplegará un navegador de archivos.
Mediante este navegador, el usuario podrá seleccionar el archivo `Json`
que desee cargar. Este comportamiento se puede ver ilustrado en la
figura [1.11](#fig:seleccionArch){reference-type="ref"
reference="fig:seleccionArch"}.

![Selección de archivo estático para aumentar los datos
disponibles[]{label="fig:seleccionArch"}](IMG/CAP7/sleccion_archiv_estatic.png){#fig:seleccionArch
width="80%"}

Después de seleccionar el archivo, se solicitará confirmación al usuario
mediante el mensaje que se representa en la figura
[1.12](#fig:confirmastatic){reference-type="ref"
reference="fig:confirmastatic"}. Tras la finalización de la
clasificación de la nueva información, se generará un archivo adicional
que será almacenado en la carpeta `/Posible_Extended_Data`. La
finalización de la asignación de contenido en este archivo, será
notificada a través de un mensaje como el ilustrado en la figura
[1.10](#fig:dataupdated){reference-type="ref"
reference="fig:dataupdated"}. Este archivo, será utilizado en adelante
por la aplicación, por lo que si se desea contemplar otros datos deberá
eliminarse o modificarse en Google Drive.

![Confirmación de cargado de datos
estáticos[]{label="fig:confirmastatic"}](IMG/CAP7/confirma_static.PNG){#fig:confirmastatic
width="30%"}

### Limitaciones para el usuario

Para finalizar con este capitulo, hace falta mencionar que el usuario
dispone de ciertas limitaciones con respecto a la obtención de datos.
Por motivos de simplicidad y para evitar posibles problemas a nivel
software, se decidió que la aplicación solo pudiese mantener, de manera
concurrente, dos hilos de ejecución. Por una parte, un hilo principal
para conservar la aplicación en estado de ejecución, y por otra, otro
hilo independiente para realizar alguna de las acciones de modificación
de datos.

En consecuencia de esto ultimo, si el usuario ya ha emprendido alguna de
las acciones disponibles para modificar el conjunto de datos, deberá
esperar a que la acción finalice para realizar una nueva acción del
mismo estilo. Por esta razón, si el usuario intenta realizar dos
acciones de modificación de datos de manera simultanea, la aplicación se
encargará de advertirle mediante el mensaje ilustrado en la figura
[1.13](#fig:limitacionesUsu){reference-type="ref"
reference="fig:limitacionesUsu"}.

![Limitaciones al actualizar los datos
[]{label="fig:limitacionesUsu"}](IMG/CAP7/Limitacion_usuario.png){#fig:limitacionesUsu
width="100%"}

[^1]: Twitter Developer:
    <https://developer.twitter.com/en/portal/products>

[^2]: Google Cloud Platform: <https://cloud.google.com/>

[^3]: Información obtenida en el paso 4 de la imagen
    [1.4](#fig:credenGdriveP1){reference-type="ref"
    reference="fig:credenGdriveP1"}

