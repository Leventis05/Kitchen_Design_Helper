# Dreaming them Kitchens

## Checklist

### Queries
- [ ] Create docker image and container for python dev
- [ ] Create python query script for search engine
- [ ] Extract and return installation instruction image

### Email processing
- [ ] Create sample pool of emails being sent
- [ ] Articulate needed tools (image recognition, text model extractor if there's more in the text than just the
product model code) to extract model code
- [ ] Return model code

### Safety checks
- [ ] Ensure manuals' guides actually match already confirmed images from a professional
- [ ] Given a possible pool of already sent (in an email) product codes, all of them (or most)
can be found by the engine - in order to also generate a success percentage for the model (or
at least part of it, since the success percentage is also affected by the image processor which
will extract the model name if only image is given PLUS our ability to find the manual image)


## Structure

1) **Email data extractor-navigator** [_EDEN_]. Takes the email and creates a list of product codes. 
2) **Query managment System** [_QuMaSy_]. Goes into manualsLib, requests the appropriate manual and gives a link to the installtion page
3) **Search model online** [_SMOl_]. On [QuMaSy](#structure) fail searches elsewhere for the installation image

## Useful Data:

### Links
- [Manuals Database](https://www.manualslib.com/)
- [Installation Guide](https://youtu.be/dQw4w9WgXcQ?si=75LoIrzOCJ3Uac2z)

### .rodata
```
μειλ με φωτο προσφορα απο τον κωτσοβολο/φωτο απο μια συσκευη κατευθειαν απο manufacturer
autorecognize μοντελο/κωδικο απο φωτο

εικονα τοποθετησης για να καταλαβεις (autorecognize)
πληρους εντοιχισμου vs εμφανες καντράν
την εικονα τοποθετησης τη βρισκω στο browser αν δεν την εχει πχ στον κωτσοβολο

has to be an exact match
```