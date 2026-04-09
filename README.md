# Mehadrin ל (Lamed) Compiler - Phase 1

This is the documentation for the **Mehadrin** transpiler. Currently, the compiler supports a "Lazy" translation mode that performs a direct token-to-token swap from Hebrew to C.

### How to Run

Use the `mehadrin` command (or your driver script) with the following flags:

```bash
# General Syntax
python mehadrin.py <filename>.ל -l -o <output_binary>

# Example
python mehadrin.py שלום_עולם.ל --lazy -o app.out

- `-l`/`--lazy`: Required for the current proof of concept. Tells the compiler to skip the full AST generation and perform a classic token to C mapping
- `-o`: (Optional) The name of the output binary
- `-k`/`--keep`: Keep the intermediate C source file

C standard library functions are currently in english only.
You should set the locale inside your main functions with `setlocale(LC_ALL, "");` if you are using hebrew strings.

You currently can't add preprocessor directives inside the .ל source, if you need a specific include add that to the file generated with -k and compile manually.



Translations:
types:
int - שלם
long - ארוך
short - קצר
void - ריק
char - תו
signed - מסומן
unsigned - לאמסומן
float - צף
double - כפול
const - קבוע
struct - מבנה
union - איחוד
typedef - הגדרסוג
enum - מספור

control flow:
break - שבור
switch - החלף
case - מקרה
continue - המשך
default - ברירתמחדל
do - עשה
while - כאשר
if - אם
else - אחרת
for - עבור
return - החזר

preprocessor directives:
define - הגדר
undef - הסר
ifdef - אםהוגדר
ifndef - אםלאהוגדר
include - כלול

misc:
extern - חיצוני
sizeof - גודלשל

stdio:
stdio.h - תקןקפ.כ
printf - הדפס
scanf - סרוק

stdlib:
stdlib.h - ספרייתתקן.כ
malloc - הקצה
realloc - הקצהמחדש
free - שחרר

string:
string.h - מחרוזת.כ
strcmp - השווהמחרוזת
strlen - אורךמחרוזת
strcpy - העתקמחרוזת
strcat - חברמחרוזת
sprintf - הדפסלמחרוזת

unistd
unistd.h - יוניקסתקן.כ
open - פתח
read - קרא
write - כתוב
close - סגור
lseek - הזזמצביע
