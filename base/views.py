# core/views.py
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework import status

from .utils import extract_text_from_image, extract_text_from_pdf, fill_template

@api_view(["POST"])
@parser_classes([MultiPartParser, FormParser, JSONParser])
def process_content(request):
    """
    Accepts:
      - text (string) OR
      - file (image/pdf) as multipart file
      - template (string, LaTeX with {{content}} placeholder)
      - languages (optional list or comma-separated string for OCR)
    Returns:
      - extracted_text
      - formatted_latex
    """
    # template = request.data.get("template", "")
    plain_text = request.data.get("text")
    uploaded_file = request.FILES.get("file")
    languages = request.data.get("languages")  # e.g., "en,hi"

    # normalize languages
    if isinstance(languages, str):
        languages = [x.strip() for x in languages.split(",") if x.strip()]
    elif not languages:
        languages = ['en']

    extracted_text = ""

    # Priority: explicit text > file OCR/extract
    if plain_text and str(plain_text).strip():
        extracted_text = str(plain_text)

    elif uploaded_file:
        name = uploaded_file.name.lower()
        data = uploaded_file.read()

        if name.endswith(".pdf"):
            extracted_text = extract_text_from_pdf(data, languages=languages)
        else:
            # treat as image
            extracted_text = extract_text_from_image(data, languages=languages)

    if not extracted_text.strip():
        return Response({"error": "No text could be extracted."}, status=status.HTTP_400_BAD_REQUEST)

    # formatted_output = fill_template(template, extracted_text)

    return Response(
        {
            "extracted_text": extracted_text,
            # "formatted_latex": formatted_output,
        },
        status=status.HTTP_200_OK,
    )
