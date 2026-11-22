# Backpack

אפליקציית ווב לטלפון: מפרקים סט לגו, מעבירים את המצלמה מעל הערימה, והאפליקציה מראה לאיזו שקית כל חלק שייך.

## מבנה

| תיקייה | מה יש בה |
|---|---|
| `bagback/site/` | **האפליקציה.** `index.html` הוא קובץ המקור היחיד, עורכים אותו ישירות. זו גם התיקייה שמתפרסמת ב-Netlify (אייקונים, `manifest.webmanifest`, `_redirects`). |
| `sets/` | הכנת נתוני סטים: `raw.json` → `gen.py` → `realsets.js`. |
| `archive/` | קבצים ישנים לעיון בלבד, לא בשימוש. |

### `archive/`
- `lego-sorter/`: אב הטיפוס הראשון (בעברית).
- `build/`: תהליך הבנייה הישן. `build.py` הרכיב את `bagback/site/index.html` מ-`template.html`, מ-`tracker.js`, מקטעים שגזר מתוך אב הטיפוס ומ-`sets/realsets.js`. הוא הוחלף בעריכה ישירה של `index.html`.

## הרצה מקומית

המצלמה עובדת רק ב-`localhost` או ב-`https`, ולכן צריך שרת מקומי ולא פתיחה ישירה של הקובץ. לדוגמה, מתוך `bagback/site`:

```
python -m http.server 8080
```

ואז לפתוח בדפדפן את http://localhost:8080/

השירותים החיצוניים (locabriques לרשימות חלקים, brickognize לזיהוי חלק מתמונה) עוברים דרך proxy רק כשהאתר רץ על `netlify.app`, כפי שמוגדר ב-`_redirects`. במקומי הדפדפן פונה אליהם ישירות, ועלול לחסום את הפנייה (CORS).

## עדכון נתוני סטים

מתוך התיקייה `sets/` מריצים:

```
python gen.py
```

הפקודה מייצרת מחדש את `realsets.js`. את התוכן שלו (`BL_PALETTE`, `REAL_SETS`, `REAL_SET_DATA`) מעתיקים ידנית לתוך `bagback/site/index.html`, במקום הבלוק הקיים.
