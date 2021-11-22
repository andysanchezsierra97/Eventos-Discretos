---
title: "Eventos Discretos"
tags: ""
---

# Happy Computing

## Andy Sánchez Sierra C-411

## Orden del problema

4. Happy Computing

Happy Computing es un taller de reparaciones electronicas se realizan las siguientes actividades (el precio de cada servicio se muestra entre parentesis:
1. Reparacion por garantıa (Gratis) 
2. Reparacion fuera de garantıa ($350) 
3. Cambio de equipo ($500) 
4. Venta de equipos reparados ($750)

Se conoce ademas que el taller cuenta con 3 tipos de empleados: Vendedor, Tecnico y Tecnico Especializado. Para su funcionamiento, cuando un cliente llega al taller, es atendido por un vendedor y en caso de que el servicio que requiera sea una Reparacion (sea de tipo 1 o 2) el cliente debe ser atendido por un tecnico (especializado o no). Ademas en caso de que el cliente quiera un cambio de equipo este debe ser atendido por un tecnico especializado. Si todos los empleados que pueden atender al cliente estan ocupados, entonces se establece una cola para sus servicios. Un tecnico especializado solo realizara Reparaciones si no hay ningun cliente que desee un cambio de equipo en la cola. Se conoce que los clientes arriban al local con un intervalo de tiempo que distribuye poisson con λ = 20 minuts y que el tipo de servicios que requieren pueden ser descrito mediante la tabla de probabilidades:

Tipo de Servicio   Probabilidad 
    1                   0.45 
    2                   0.25 
    3                   0.1 
    4                   0.2

Ademas se conoce que un tecnico tarda un tiempo que distribuye exponecial con λ = 20 minutos, en realizar una Reparacion Cualquiera. Un tecnico especializdo tarda un tiempo que distribuye exponencial con λ = 15 minutos para realizar un cambio de equipos y la vendedora puede atender cualquier servicio en un tiempo que distribuye normal (N(5 min, 2mins)). El dueño del lugar desea realizar una simulacion de la ganancia que tendrıa en una jornada laboral si tuviera 2 vendedores, 3 tecnicos y 1 tecnico especializado.


## Descripcion

La idea general utilizada para resolver el problema fue realizar 6 servidores en paralelos:
2 Servidores para los Vendedores
1 Servodor para el Tecnico especializado
3 Servidores para los Tecnicos

Cuando llega un cliente, si necesita la venta de un equipo, si uno de los dos vendedores no esta ocupado pasa a ser atendido, en caso contrario pasa a una cola de personas pendientes a servicio de venta de equipo.

Si el cliente necesita un cambio de equipo, si el tecnico especializado no esta ocupado pasa a ser atendido, en caso contrario pasa a una cola de personas pendientes a servicios de cambio de eqiupo.

Si el cliente necesita una reparacion, si hay tecnicos pendientes, pasa a ser atendido, en caso contrario se verifica que el tecnico especializaso no este ocupado y no exista nadie en la cola de pendientes a cambio de equipo, en caso contrario pasa a una cola de personas pendientes a servicio de reparacion de equipo.

Variables de Tiempo:

t - tiempo general
ta - tiempo de arribo
T - jornada laboral(480 min)

Vendedores:
tDv1 - tiempo de salida del servido de vendedores 1
tDv2 - tiempo de salida del servido de vendedores 2

Especializado: 
tDe - tiempo de salida del servido de tecnico especializado

Tecnicos:
tDt1 - tiempo de salida del servido de tecnicos 1
tDt2 - tiempo de salida del servido de tecnicos 2
tDt3 - tiempo de salida del servido de tecnicos 3

Variables Contadoras:

G - ganacia

Na - cantidad de arribos
A - diccionario de arribo:tiempo de arribo

Vendedores:
nv - numero de clientes de servicio de venta en el sistema
NDv1 - cantidad de partidas de clientes de servicio de venta en el sistema en el servidor 1(SV1)
NDv2 - cantidad de partidas de clientes de servicio de venta en el sistema en el servidor 2(SV2)
Dv1 - diccionario de salida:tiempo de salida de clientes de servicio de venta en el sistema en el servidor 1
Dv2 - diccionario de salida:tiempo de salida de clientes de servicio de venta en el sistema en el servidor 2

Especializado
ne - numero de clientes de servicio de cambio en el sistema
NDe - cantidad de partidas de clientes de servicio de cambio en el sistema en el servidor(SE)
De - diccionario de salida:tiempo de salida de clientes de servicio de cambio en el sistema en el servidor

Tecnicos
nt - numero de clientes de servicio de reparacion en el sistema
NDt1 - cantidad de partidas de clientes de servicio de reparacion en el sistema en el servidor 1(ST1)
NDt2 - cantidad de partidas de clientes de servicio de reparacion en el sistema en el servidor 2(ST2)
NDt3 - cantidad de partidas de clientes de servicio de reparacion en el sistema en el servidor 3(ST3)
Dv1 - diccionario de salida:tiempo de salida de clientes de servicio de reparacion en el sistema en el servidor 1
Dt2 - diccionario de salida:tiempo de salida de clientes de servicio de reparacion en el sistema en el servidor 2
Dt3 - diccionario de salida:tiempo de salida de clientes de servicio de reparacion en el sistema en el servidor 3

Variables de estado:

ST = [nt, i1, i2, i3, qt] (i1=cliente en ST1, i2=cliente en ST2, i3=cliente en ST3, qt = cola del servidores de servicio de reparacion)
SV =[nv,i1,i2,qv] (i1=cliente en SV1, i2=cliente en SV2, qv = cola del servidores de servicio de venta)
SE [ns,i1,qe] (i1=cliente en SE, qe = cola del servidores de servicio de cambio)

## Consideraciones
A partir de la ejecucion de las simulaciones del problema se puede percatar que la mayor cantidad de clientes que llegan al taller es para una reparacion con garantia y esta es gratuita, ademas los servicios de reparacion, es mas probable que la haga un tecnico y este proceso distribuye exponecial con λ = 20 minutos.
El sevicio mas costoso es el de venta de equipos pero que este distribuye normal (N(5 min, 2mins)).
