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

המצלמה עובדת רק ב-`localhost` או ב-`https`, ולכן צריך שרת מקומי ולא פתיחה ישירה של הקובץ. מתוך תיקיית הפרויקט:

```
powershell -ExecutionPolicy Bypass -File tools\dev-server.ps1
```

ואז לפתוח בדפדפן את http://localhost:8080/

השרת לא דורש התקנה של Node או Python. הוא גם מחקה את ה-`_redirects` של Netlify: הוא מעביר את `/lb/` ל-locabriques ואת `/bk/` ל-brickognize. בלי זה הדפדפן חוסם את הפניות ל-locabriques (CORS), וטעינת סטים לפי מספר לא עובדת.

## עדכון נתוני סטים

מתוך התיקייה `sets/` מריצים:

```
python gen.py
```

הפקודה מייצרת מחדש את `realsets.js`. את התוכן שלו (`BL_PALETTE`, `REAL_SETS`, `REAL_SET_DATA`) מעתיקים ידנית לתוך `bagback/site/index.html`, במקום הבלוק הקיים.
