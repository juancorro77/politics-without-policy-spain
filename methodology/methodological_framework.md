# Marco Metodológico: Medición de la Tasa de Evasión y Desplazamiento de Agenda en el Control Parlamentario

Este documento sistematiza la fundamentación científica, los precedentes en la literatura académica y la fórmula de operacionalización para medir la desviación entre el **tema manifiesto** (la pregunta formal registrada) y el **tema latente** (el debate real en tribuna) en las Sesiones de Control del Congreso de los Diputados de España, utilizando indicadores estandarizados de la ciencia política.

---

## 1. Justificación del Marco de Análisis

En los sistemas parlamentarios de corte Westminster o de alta polarización bipolar (como España), las preguntas orales en las Sesiones de Control al Gobierno sufren frecuentemente un fenómeno de **desvío estratégico de agenda**. Una iniciativa registrada formalmente bajo una temática de gestión sectorial (ej. vivienda, energía, infraestructuras) es instrumentalizada por los oradores (tanto de la oposición como del Gobierno) como una percha formal para entablar un debate ajeno al tema de origen, centrado en la confrontación por el poder, las reglas de juego constitucionales o pactos políticos.

En lugar de acuñar índices ad-hoc no validados por la academia, este estudio adopta dos métricas ampliamente extendidas y validadas en la literatura de la ciencia política y la lingüística política:
1.  **La Tasa de Evasión (Evasion Rate - ER)**: Proporción de intervenciones o unidades discursivas que eluden responder o abordar el tema técnico consultado.
2.  **La Tasa de Desplazamiento de Agenda (Agenda Shift Rate - ASR)**: Frecuencia con la que se altera activamente el marco temático (*frame*) original de la pregunta para reenfocarlo en la confrontación partidista o territorial.

---

## 2. Fundamentación en la Literatura Científica

La medición del desvío temático en sede parlamentaria está firmemente respaldada por las siguientes corrientes de investigación:

### A. La codificación de la evasión y las "no-respuestas" (Evasion / Non-Replies)
*   **Bull y Mayer (1993)** y **Bull (2003)** definieron el marco fundacional para codificar la evasión en el discurso político. Su tipología identifica 11 métodos de evasión (como *atacar la pregunta*, *redefinir el tema* o *hacer ataques personales*). La **Tasa de Evasión** es el porcentaje de turnos de palabra donde se identifica alguna de estas estrategias frente a las respuestas directas.
*   **Rasiah (2010)** adaptó estas tipologías al *Question Time* parlamentario. Desarrolló el concepto de **desplazamiento de agenda (Agenda Shift)**, clasificándolo como una evasión encubierta donde el orador ignora la agenda de la pregunta e impone una agenda propia de confrontación.

### B. El conflicto sobre "Politics" vs. "Policy"
*   **Bara, Weale y Bicquelet (2007)** establecieron metodologías para dividir sistemáticamente las actas de debate en enunciados referidos a **policy** (análisis técnico de la política pública, asignación presupuestaria, gestión de servicios) frente a enunciados referidos a **politics** (táctica de partido, legitimidad de alianzas, descalificación ideológica). El ratio resultante se emplea para evaluar la calidad deliberativa del parlamento.
*   **Green-Pedersen (2010)**, utilizando los códigos del *Comparative Agendas Project (CAP)*, demostró que la oposición utiliza el control parlamentario para forzar encuadres conflictivos en lugar de debates informativos, buscando el desgaste reputacional del Gobierno.
*   **Hood (2011)** describió el fenómeno de *Blame Avoidance* (evitación de la culpa), por el cual el Ejecutivo utiliza su turno de réplica no para informar, sino para desviar la responsabilidad hacia otros actores (antiguos gobiernos, gobiernos autonómicos), desplazando el foco temático.

### C. El caso español: Confrontación y gesticulación
*   **Maurer (2008)** y otros estudios nacionales del CIS analizan las Sesiones de Control del Congreso de los Diputados. Concluyen que el diseño reglamentario y la cultura política en España han convertido este espacio en un "juego de suma cero" donde el contenido técnico de las preguntas es secundario frente a su rentabilidad electoral e impacto mediático inmediato.

---

## 3. Metodología y Operacionalización

Para auditar las sesiones, cada intercambio parlamentario $i$ (compuesto por la intervención del diputado y la del miembro del Gobierno) se evaluará bajo el siguiente esquema:

### Fase 1: Clasificación del Tema Manifiesto (CAP)
Se asigna el tema de política pública formal de la pregunta (según la codificación oficial del *Comparative Agendas Project*):
*   Vivienda, Energía, Transporte, Educación, Sanidad, etc.

### Fase 2: Segmentación y Codificación del Discurso Real (Latente)
El texto completo de la transcripción oral del intercambio se divide en **Unidades de Discurso (UD)** (correspondientes a oraciones o párrafos coherentes). Cada UD se codifica de forma dicotómica:

1.  **UD de Gestión y Resultados (Policy)**: Contenido referido a presupuestos reales, plazos, impacto normativo, detalles de leyes sectoriales, datos del servicio público, o problemas de gestión técnica.
2.  **UD de Lucha por el Poder (Politics)**: Contenido referido a pactos de investidura, amnistías, disputas de representatividad, legitimidad territorial, reparto de sillones, contranarrativas de partido o ataques morales de corrupción.

### Fase 3: Cálculo de la Tasa de Evasión de la Agenda (Agenda Shift Rate - ASR)
Para un intercambio $i$ cuyo tema manifiesto es de *Gestión* (Policy), la **Tasa de Desplazamiento de Agenda ($ASR_i$)** se define como la proporción de unidades discursivas que abandonan el debate técnico para centrarse en la agenda de poder:

$$ASR_i = \frac{UD_{\text{Politics}, i}}{UD_{\text{Politics}, i} + UD_{\text{Policy}, i}} \times 100$$

*   Un $ASR_i = 0\%$ representa un debate plenamente alineado con la gestión de la política pública.
*   Un $ASR_i = 100\%$ representa una evasión total del tema original, donde el intercambio formalmente sectorial se convierte íntegramente en un debate sobre el poder y las reglas de juego.

La **Tasa de Evasión de Agenda de la Sesión** ($ASR_{\text{Sesión}}$) se obtiene mediante la media ponderada del desplazamiento temático de todos sus intercambios individuales.

---

## 4. Referencias Bibliográficas

1.  **Bara, J., Weale, A., & Bicquelet, A. (2007)**. *Analyzing parliamentary debate: How and why?* Quality & Quantity, 41, 577-597.
2.  **Bull, P., & Mayer, K. (1993)**. *How Winston Churchill and Margaret Thatcher evade questions in political interviews*. Journal of Language and Social Psychology, 12(4), 270-288.
3.  **Bull, P. (2003)**. *The Microanalysis of Political Communication: Claptrap and Equivocation*. Psychology Press.
4.  **Clayman, S. E. (2001)**. *Answers and evasions*. Language in Society, 30(3), 403-442.
5.  **Green-Pedersen, C. (2010)**. *Who sets the agenda in parliamentary government? Defining the role of opposition and government in parliamentary questions*. European Journal of Political Research, 49(3), 347-369.
6.  **Hood, C. (2011)**. *The Blame Game: Spin, Bureaucracy, and Self-Preservation in Government*. Princeton University Press.
7.  **Maurer, L. M. (2008)**. *El poder de control del Parlamento: Las preguntas al Gobierno en el Congreso de los Diputados*. Centro de Investigaciones Sociológicas (CIS).
8.  **Rasiah, R. (2010)**. *A framework for the systematic coding of evasion in parliamentary question time*. Journal of Pragmatics, 42(3), 664-680.
