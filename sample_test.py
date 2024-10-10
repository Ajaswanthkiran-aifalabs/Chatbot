from googletrans import Translator

translator=Translator(service_urls=['translate.googleapis.com'],raise_exception=True)

a=translator.detect(text="తెలుగు")

b=translator.translate("Hellooo", dest="te")
print(b)

print(a)