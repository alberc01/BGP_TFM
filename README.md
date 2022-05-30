# BGP_TFM
Introducción
============

Internet es una herramienta que proporciona multitud de servicios a la
sociedad a través de diversos protocolos de comunicación. Cada uno de
estos protocolos, con funciones determinadas, hacen posible el
funcionamiento de la fuente de información más grande del mundo. Es
complejo conseguir la coordinación de cada uno de los elementos de
Internet, en ocasiones los protocolos encargados de dicha tarea incluyen
características de configuración que pueden afectar a su correcto
funcionamiento.

Según la función que desempeñen, los protocolos de red se pueden
clasificar mediante el modelo OSI (*Open System Interconnection*). De
esta forma, si se busca establecer comunicación entre dos nodos o
dispositivos en una red de comunicación, este modelo define las
diferentes etapas que deberán atravesar los datos para su envío. La capa
de red contemplada en este modelo se encarga del direccionamiento lógico
y mediante protocolos como IP (*Internet Protocol*) u OSPF (*Open
Shortest Path First*) determina la mejor ruta para el envío óptimo de
los datos.

El objetivo principal de este trabajo es el estudio del protocolo BGP.
No existe un criterio único para posicionar este protocolo en una de las
capas del modelo OSI. Este protocolo se encarga de la construcción de
las rutas globales de Internet, permitiendo alcanzar a cada uno de los
destinos presentes en la red. La tarea que realiza BGP es esencial para
el correcto funcionamiento de Internet, sin embargo y como se verá más
adelante, tiene algunas peculiaridades que son dignas de estudio.

Motivación
----------

Internet se puede ver como un gran grafo, donde los vértices serían los
encargados de gestionar y realizar el intercambio de la información. Uno
de los protocolos más importantes para poder realizar esta tarea es BGP.

Este protocolo proporciona mecanismos para el intercambio de información
de encaminamiento entre los diferentes sistemas que componen la red.
Dentro de la terminología BGP, los nodos que componen una red BGP se
denominan Sistemas Autónomos (AS, *Autonomous System*), los cuales se
identifican mediante un número único o ASN (*Autonomous System Number*).

De esta forma, el protocolo se encarga de establecer las rutas óptimas
por las cuales el tráfico será dirigido. Para poder establecer estas
rutas, el propio protocolo dota de diferentes opciones de configuración
que se gestionan de manera local por diferentes AS. Sin embargo, queda
por definir que es una ruta óptima, puesto que cada sistema autónomo
puede tener unos intereses particulares distintos.

La gran versatilidad a la hora de configurar y determinar las diferentes
rutas que seguirá el tráfico de red significa un gran beneficio a favor
del protocolo BGP. Sin embargo, como se trata de una herramienta de
carácter global cuya gestión se realiza de manera local, existe el
riesgo de que se pueda manipular en pro de diferentes intereses
económicos y geopolíticos.

Debido a esto ultimo, se pueden encontrar multitud de estudios que
pretenden identificar cuando uno de estos Sistemas Autónomos no trabaja
como debería, es decir, cuando el sistema no intercambia la información
adecuada debido a una mala configuración local, ya sea de forma
deliberada o no.

De la misma forma, también existen herramientas a disposición del
público que se encargan de monitorizar las actualizaciones BGP, tratando
de determinar un posible anuncio fraudulento (*Hijack*), una posible
caída de servicio (*Outage*) o una filtración indebida de prefijos (*BGP
Leak*) durante el intercambio de información entre los Sistemas
Autónomos.

BGPStream [@orsini2016bgpstream] es un producto de la compañía Cisco
Systems [@cisco]. Esta herramienta, mediante la plataforma social
Twitter, publica información relevante acerca de los eventos que puedan
significar algún riesgo relacionado con BGP.

A lo largo de la historia de BGP se han podido experimentar multitud de
problemas como consecuencia de una mala configuración, produciendo un
cambio sustancial en el tránsito del tráfico de red o la inaccesibilidad
a Internet. Un ejemplo de estas consecuencias se pudo ver el 4 de
Octubre de 2021 [@bgp-facebook], donde Facebook debido a una mala
configuración de las tablas de rutas de BGP quedó inaccesible a través
de Internet, produciendo la caída en cadena de las redes sociales
(Whatsapp e Instagram) más utilizadas por los usuarios y la interrupción
del servicio de otras empresas dependientes de Facebook como proveedor.

Este es solo un ejemplo de los posibles problemas que puede presentar
este protocolo de encaminamiento, pero existen muchos otros de gran
relevancia. En la actualidad se puede entrever que los datos y la
información que transitan por la red cobran cada vez más importancia
debido a multitud de intereses económicos, sociales, políticos, etc. Si
se enfoca este problema desde un punto de vista internacional, una
alteración en el tránsito del tráfico de red puede significar una
sustracción de información sensible para las diferentes entidades
geopolíticas mundiales o su aislamiento en Internet.

Objetivos
---------

En el presente TFM se presenta un sistema de recomendación en forma de
aplicación, la cual se ha denominado BgpRS (*BGP Recommendation
System*). Esta aplicación, mediante los datos publicados por
Cisco [@cisco], proporciona recomendaciones para la configuración de
*routers* BGP con el fin de intentar evitar aquellos Sistemas Autónomos
que puedan significar algún riesgo. Además, BgpRS proporciona
herramientas para la visualización de datos, habilitando al usuario de
la capacidad de realizar un estudio histórico sobre los diferentes
eventos sucedidos en BGP. Por ejemplo, la presente guerra entre la
Federación Rusa y Ucrania puede servir como guía para observar que BGP
no es un simple protocolo de red. Los Sistemas Autónomos de estos países
producen eventos como los mencionados anteriormente de manera diaria. Si
mediante BgpRS se seleccionan diferentes momentos en el tiempo antes y
después de la guerra, y se comparan los sucesos BGP de cada uno de estos
países, se puede visualizar el impacto que tiene la guerra sobre
Internet.

Los errores de configuración de los *routers* BGP, pueden desencadenar
interrupciones de tráfico o el desvío del mismo. Por esta razón, surge
la idea de clasificar los Sistemas Autónomos según su histórico de
incidentes. Las tendencias obtenidas a través de los datos sobre los
eventos, permiten que la aplicación BgpRS informe a los administradores
BGP sobre la forma más adecuada para tratar a un Sistema Autónomo cuyo
comportamiento es errático, utilizando para ello instrucciones `vtysh`
contempladas en Quagga o FRRouting y que son fácilmente aplicables a
Cisco CLI [@cisco].

Plan de trabajo
---------------

En el protocolo BGP se producen numerosos eventos durante su
funcionamiento, aparición o desaparición de rutas, incorporación nuevos
AS, etc. En este trabajo, no es necesario el uso de cada uno de estos
eventos, ya que solo se necesitan aquellos que impliquen una caída de
servicio (*Outage*) o un cambio en el origen de prefijos (*Hijack*).

La extracción de estos datos supone un requisito necesario para la
realización de este trabajo. Sin embargo, cabe destacar que el filtrado
y la clasificación de los datos requiere de un gran número de recursos
no disponibles y que son accesibles, por ejemplo, mediante *BGP Looking
Glasses*. Por dicha razón, esta tarea será realizada por las
herramientas BGPStream [@orsini2016bgpstream] y BGPMon [@yan2009bgpmon],
y mediante el uso de la información que estas proporcionan será posible
mantener un histórico consistente que servirá a la aplicación BgpRS.

Las herramientas de Cisco [@cisco] anteriormente citadas, por una parte
se encargan de nutrir su propia base de datos histórica, sin embargo, el
acceso a estos datos se realiza a traves de su API de pago. Por otro
lado, Cisco también publica en Twitter de forma gratuita la información
de los eventos que identifica mediante estas herramientas. Uno de los
objetivos de este trabajo es proporcionar una opción gratuita para el
estudio de los eventos que se producen en BGP. Esto se puede realizar a
través de la extracción de la información disponible en Twitter, por lo
que la API de esta red social es una herramienta adicional para obtener
gran parte de la información necesaria.

Con toda la información recopilada, se procederá a realizar una
clasificación por países de los eventos, asociando el evento con el AS
que lo produjo y la organización al mando. De esta forma, se podrá
visualizar el impacto o las tendencias internacionales de utilizar BGP
como medio para cubrir intereses particulares.

Por último, a través de los diferentes datos obtenidos se procederá a
construir el mencionado Sistema de Recomendación BGP. Este sistema será
capaz de determinar cómo de necesario es tomar medidas para un AS
concreto, proporcionando instrucciones de configuración para evitar
redirigir el tráfico por aquellos AS que hayan sido considerados como no
fiables.

Puesta en marcha de la aplicación {#cap:APLICACION}
=================================

A lo largo de esta memoria se han podido visualizar las características
de la aplicación BgpRS. Por una parte, en el capitulo
[\[cap:infobgp\]](#cap:infobgp){reference-type="ref"
reference="cap:infobgp"}, se han explicado los aspectos relevantes para
extraer información de BGP. Además, se ha podido ver que esta
información es fundamental para la aplicación, dando servicio a las
funcionalidades vistas en los capítulos
[\[cap:asnPaises\]](#cap:asnPaises){reference-type="ref"
reference="cap:asnPaises"} y
[\[cap:sistemasRecomendacionBGP\]](#cap:sistemasRecomendacionBGP){reference-type="ref"
reference="cap:sistemasRecomendacionBGP"}. Para hacer todo esto posible,
BgpRS utiliza multitud de servicios.

Estos servicios son accesibles a través de diferentes librerías
disponibles en Python, por lo que será necesario instalar ciertas
dependencias antes de poder ejecutar BgpRS. En los apéndices de la
memoria se proporciona un enlace al código de BgpRS, dentro de este
proyecto se encuentra la carpeta denominada
`/dependencies_installation_dir` que contiene el archivo
`requirements.txt` con la información de las dependencias necesarias.

Conociendo todo esto y teniendo en cuenta que BgpRS actualmente solo
esta preparado para funcionar en distribuciones de Linux, se debe
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
Developer* se asemejará al representado en la figura
[1.3](#fig:twitDevACC){reference-type="ref" reference="fig:twitDevACC"}.

![Permisos *Academic Research* en Twitter, *fuente:
<https://developer.twitter.com/en/portal/products>*[]{label="fig:twitDevACC"}](Imagenes/Bitmap/academic_research_plan.PNG){#fig:twitDevACC
width="100%"}

### Asignación de credenciales dentro de BgpRS

Una vez obtenido el acceso al plan *Academic Research*, será posible
obtener las credenciales necesarias para que TweePy [@tweepy] pueda
ejecutar las solicitudes de BgpRS. El acceso a estas credenciales y su
lectura se puede realizar a través del portal *developer* de Twitter tal
y como se representa en la figura
[1.3](#fig:twitDevACC){reference-type="ref" reference="fig:twitDevACC"}.

![Acceso a credenciales de Twitter, *fuente:
<https://developer.twitter.com/en/portal/projects/1495420932801785863/apps/23448073/keys>*[]{label="fig:twitDevACC"}](Imagenes/Bitmap/Credenciales_Twitter_web.PNG){#fig:twitDevACC
width="1.\textwidth"}

Con estas credenciales en nuestra posesión, ya solo se necesita
especificar su valor dentro del código de BgpRS. Esto se debe realizar
mediante la modificación del archivo `twitterDevCredentials.py` situado
en la carpeta `/API_classes`, asignando valor a cada una de las
variables mostradas en la figura
[1.3](#fig:twitDevACC){reference-type="ref" reference="fig:twitDevACC"}.

![Archivo en BgpRS para introducir las credenciales de
Twitter[]{label="fig:twitDevACC"}](Imagenes/Bitmap/Credenciales_Twitter.PNG){#fig:twitDevACC
width="80%"}

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
<https://console.cloud.google.com/apis/credentials?authuser=1&project=phrasal-clover-312717>*[]{label="fig:credenGdriveP1"}](Imagenes/Bitmap/Credenciales_gdrive.png){#fig:credenGdriveP1
width="100%"}

En la figura [1.4](#fig:credenGdriveP1){reference-type="ref"
reference="fig:credenGdriveP1"} se representa el proceso para crear y
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
la representada en la figura
[1.5](#fig:distribuGdrive){reference-type="ref"
reference="fig:distribuGdrive"}. El nombre de estas carpetas no tiene
porque ser idéntico, ya que de estas, como se vera mas adelante, solo se
utilizará el identificador de las mismas.

![Distribución de carpetas en Google Drive, *fuente:
<https://drive.google.com/drive/u/1/folders/1dwxWQoyJvVZeOto3X0QjDy3VhQ6jhmuL>*[]{label="fig:distribuGdrive"}](Imagenes/Bitmap/Distribu_gdrive.PNG){#fig:distribuGdrive
width="100%"}

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
[1.6](#fig:folderids){reference-type="ref" reference="fig:folderids"}.

![Obtención de identificadores de carpeta, *fuente:
<https://drive.google.com/drive/u/1/folders/1pV892qsDAl28h7ivBVX3PqiMeF1oQmNK>*[]{label="fig:folderids"}](Imagenes/Bitmap/Folder_ids_gdrive.PNG){#fig:folderids
width="100%"}

Una vez obtenidos cada uno de los identificadores, solo hace falta
indicarlos en la parte correspondiente del código de BgpRS. Esta
asignación, debe realizarse en el archivo `Data_classifier_class.py` que
se encuentra situado dentro de la carpeta `/API_classes`. Según esto
ultimo, el valor de estos identificadores de carpeta se deberá indicar
sobre las variables que se resaltan en rojo en la figura
[1.7](#fig:IDSBGPRSGDRIVE){reference-type="ref"
reference="fig:IDSBGPRSGDRIVE"}.

![Asignación de identificadores de carpeta en
BgpRS[]{label="fig:IDSBGPRSGDRIVE"}](Imagenes/Bitmap/Carpetas_gDrive_bgpRS.PNG){#fig:IDSBGPRSGDRIVE
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
BgpRS[]{label="fig:accesorapid"}](Imagenes/Bitmap/iface_bgp_datos.png){#fig:accesorapid
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
datos.[]{label="fig:ejecucionUPDATE"}](Imagenes/Bitmap/Ejecuta_update.PNG){#fig:ejecucionUPDATE
width="80%"}

Como se puede observar, en primer lugar se le preguntará al usuario si
realmente quiere actualizar los datos. Después de que el usuario de
confirmación, el proceso de actualizado comenzará y al finalizar
notificará al usuario a través del mensaje reflejado en la figura
[1.10](#fig:dataupdated){reference-type="ref"
reference="fig:dataupdated"}.

![Mensaje de notificación sobre el actualizado de
datos[]{label="fig:dataupdated"}](Imagenes/Bitmap/data_updated_msg.png){#fig:dataupdated
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
disponibles[]{label="fig:seleccionArch"}](Imagenes/Bitmap/sleccion_archiv_estatic.png){#fig:seleccionArch
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
estáticos[]{label="fig:confirmastatic"}](Imagenes/Bitmap/confirma_static.PNG){#fig:confirmastatic
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
[]{label="fig:limitacionesUsu"}](Imagenes/Bitmap/Limitacion_usuario.png){#fig:limitacionesUsu
width="100%"}

\@bookKonstantinos, author = Konstantinos Arakadakis, title = BGPstream
events analysis, url =
https://gitlab.com/konstantinosarakadakis/BGPstream/-/tree/master

\@techreportbgp-facebook, day = 5, month = Octubre, year = 2021, url =
https://www.elmundo.es/tecnologia/2021/10/05/615c1d92fc6c8324028b45df.html,
urldate = 2022-05-09TZ, title = Los culpables de la caída de Facebook,
WhatsApp e Instagram: el BGP y las DNS, author = Bruno Toledano

\@techreportpaises-datos, type = Dataset, year = 2012, month = December,
url = https://datahub.io/core/country-list, title = List of all
countries with their 2 digit codes (ISO 3166-1)

\@techreportpycountry, author = Theune C., type = Python library, title
= ISO country, subdivision, language, currency and script definitions
and their translations, url = https://pypi.org/project/pycountry/

\@bookhurricane, author = Hurricane Electric, title = Hurricane
Electric's Network Looking Glass, url = https://lg.he.net/

\@bookreiris, author = RedIRIS NOC, title = RedIRIS Looking glass, url =
https://www.rediris.es/red/lg/

\@techreportselenium, type = Selenium Documentation, year = 2011-2018,
url = https://selenium-python.readthedocs.io/, title = Selenium with
Python, license = License: This document is licensed under a Creative
Commons Attribution-ShareAlike 4.0 International License
\<http://creativecommons.org/licenses/by-sa/4.0/\>, author = Muthukadan
B.

\@bookPython, author = Van Rossum, Guido and Drake, Fred L., title =
Python 3 Reference Manual, year = 2009, isbn = 1441412697, publisher =
CreateSpace, address = Scotts Valley, CA, url = https://www.python.org/

\@techreportISO13586, type = Standard, key = ISO 3166-1:2020(en), year =
2020, url = https://www.iso.org/obp/ui/\#iso:std:iso:3166:-1:ed-4:v1:en,
title = Codes for the representation of names of countries and their
subdivisions -- Part 1: Country code \@techreportpydrive, type = Python
Library Documentation, key = PyDrive documentation, year = 2016, url =
https://pythonhosted.org/PyDrive/, title = PyDrive documentation, author
= JunYoung Gwak and Scott Blevins and Robin Nabel and Google Inc.

\@techreporttweepy, type = Python Library Documentation, key = Tweepy
Documentation, year = 2009-2022, url =
https://docs.tweepy.org/en/stable/, title = Tweepy Documentation, author
= Roesslein J.

\@inproceedingsorsini2016bgpstream, title=BGPStream: a software
framework for live and historical BGP data analysis, author=Orsini,
Chiara and King, Alistair and Giordano, Danilo and Giotsas, Vasileios
and Dainotti, Alberto, doi = 10.1145/2987443.2987482,
booktitle=Proceedings of the 2016 Internet Measurement Conference,
pages=429--444, year=2016

\@inproceedingsyan2009bgpmon, title=BGPmon: A real-time, scalable,
extensible monitoring system, author=Yan, He and Oliveira, Ricardo and
Burnett, Kevin and Matthews, Dave and Zhang, Lixia and Massey, Dan,
booktitle=2009 Cybersecurity Applications & Technology Conference for
Homeland Security, pages=212--223, doi = 10.1109/CATCH.2009.28,
year=2009, organization=IEEE

\@miscrfc1058, series = Request for Comments, number = 1058,
howpublished = RFC 1058, publisher = RFC Editor, doi = 10.17487/RFC1058,
url = https://www.rfc-editor.org/info/rfc1058, author = C.L. Hedrick,
title = Routing Information Protocol, pagetotal = 33, year = 1988, month
= jun, abstract = This RFC describes an existing protocol for exchanging
routing information among gateways and other hosts. It is intended to be
used as a basis for developing gateway software for use in the Internet
community.,

\@miscrfc1105, series = Request for Comments, number = 1105,
howpublished = RFC 1105, publisher = RFC Editor, doi = 10.17487/RFC1105,
url = https://www.rfc-editor.org/info/rfc1105, author = K. Lougheed and
Y. Rekhter, title = Border Gateway Protocol (BGP), pagetotal = 17, year
= 1989, month = jun, abstract = This RFC outlines a specific approach
for the exchange of network reachability information between Autonomous
Systems. Updated by RFCs 1163 and 1164. \[STANDARDS-TRACK\],

\@miscrfc1163, series = Request for Comments, number = 1163,
howpublished = RFC 1163, publisher = RFC Editor, doi = 10.17487/RFC1163,
url = https://www.rfc-editor.org/info/rfc1163, author = Lougheed, K. and
Y. Rekhter, title = Border Gateway Protocol (BGP), pagetotal = 29, year
= 1990, month = jun, abstract = This RFC, together with its companion
RFC-1164, \"Application of the Border Gateway Protocol in the
Internet\", specify an inter-autonomous system routing protocol for the
Internet. \[STANDARDS-TRACK\],

\@miscrfc1265, series = Request for Comments, number = 1265,
howpublished = RFC 1265, publisher = RFC Editor, doi = 10.17487/RFC1265,
url = https://www.rfc-editor.org/info/rfc1265, author = Yakov Rekhter,
title = BGP Protocol Analysis, pagetotal = 8, year = 1991, month = oct,
abstract = This report summarizes the key feature of BGP, and analyzes
the protocol with respect to scaling and performance. This memo provides
information for the Internet community. It does not specify an Internet
standard.,

\@miscrfc1267, series = Request for Comments, number = 1267,
howpublished = RFC 1267, publisher = RFC Editor, doi = 10.17487/RFC1267,
url = https://www.rfc-editor.org/info/rfc1267, author = Lougheed, K. and
Y. Rekhter, title = Border Gateway Protocol 3 (BGP-3), pagetotal = 35,
year = 1991, month = oct, abstract = This memo, together with its
companion document, \"Application of the Border Gateway Protocol in the
Internet\", define an inter-autonomous system routing protocol for the
Internet. \[STANDARDS-TRACK\],

\@miscrfc1654, series = Request for Comments, number = 1654,
howpublished = RFC 1654, publisher = RFC Editor, doi = 10.17487/RFC1654,
url = https://www.rfc-editor.org/info/rfc1654, author = Yakov Rekhter
and Tony Li, title = A Border Gateway Protocol 4 (BGP-4), pagetotal =
56, year = 1994, month = jul, abstract = This document defines an
inter-autonomous system routing protocol for the Internet.
\[STANDARDS-TRACK\],

\@miscrfc1771, series = Request for Comments, number = 1771,
howpublished = RFC 1771, publisher = RFC Editor, doi = 10.17487/RFC1771,
url = https://www.rfc-editor.org/info/rfc1771, author = Rekhter, Y. and
T. Li, title = A Border Gateway Protocol 4 (BGP-4), pagetotal = 57, year
= 1995, month = mar, abstract = This document, together with its
companion document, \"Application of the Border Gateway Protocol in the
Internet\", define an inter-autonomous system routing protocol for the
Internet. \[STANDARDS-TRACK\],

\@misccisco, author = Cisco Systems, Inc,
url=https://crosswork.cisco.com/, title=Cisco Crosswork Cloud

\@miscredes, author = Fabero Jiménez, J.C., publisher = Universidad
Complutense de Madrid, title =Máster en Ingeniería Informática.
Encaminamiento externo: BGPv4. Asignatura: Redes de Nueva Generación,
pagetotal = 104,

\@miscrfc4264, series = Request for Comments, number = 4264,
howpublished = RFC 4264, publisher = RFC Editor, doi = 10.17487/RFC4264,
url = https://www.rfc-editor.org/info/rfc4264, author = Tim A. Griffin
and Geoff Huston, title = BGP Wedgies, pagetotal = 10, year = 2005,
month = nov, abstract = It has commonly been assumed that the Border
Gateway Protocol (BGP) is a tool for distributing reachability
information in a manner that creates forwarding paths in a deterministic
manner. In this memo we will describe a class of BGP configurations for
which there is more than one potential outcome, and where forwarding
states other than the intended state are equally stable. Also, the
stable state where BGP converges may be selected by BGP in a
non-deterministic manner. These stable, but unintended, BGP states are
termed here \"BGP Wedgies\". This memo provides information for the
Internet community.,

\@miscrfc4271, series = Request for Comments, number = 4271,
howpublished = RFC 4271, publisher = RFC Editor, doi = 10.17487/RFC4271,
url = https://www.rfc-editor.org/info/rfc4271, author = Yakov Rekhter
and Susan Hares and Tony Li, title = A Border Gateway Protocol 4
(BGP-4), pagetotal = 104, year = 2006, month = jan, abstract = This
document discusses the Border Gateway Protocol (BGP), which is an
inter-Autonomous System routing protocol. The primary function of a BGP
speaking system is to exchange network reachability information with
other BGP systems. This network reachability information includes
information on the list of Autonomous Systems (ASes) that reachability
information traverses. This information is sufficient for constructing a
graph of AS connectivity for this reachability from which routing loops
may be pruned, and, at the AS level, some policy decisions may be
enforced. BGP-4 provides a set of mechanisms for supporting Classless
Inter-Domain Routing (CIDR). These mechanisms include support for
advertising a set of destinations as an IP prefix, and eliminating the
concept of network \"class\" within BGP. BGP-4 also introduces
mechanisms that allow aggregation of routes, including aggregation of AS
paths. This document obsoletes RFC 1771. \[STANDARDS-TRACK\],

\@articleopenBMP, title=Bgp monitoring protocol (bmp), author=Scudder,
John and Fernando, Rex and Stuart, Stephen, journal=Internet Engineering
Task Force, pages=1--27, year=2016

[^1]: Twitter Developer:
    <https://developer.twitter.com/en/portal/products>

[^2]: Google Cloud Platform: <https://cloud.google.com/>

[^3]: Información obtenida en el paso 4 de la imagen
    [1.4](#fig:credenGdriveP1){reference-type="ref"
    reference="fig:credenGdriveP1"}
