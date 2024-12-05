from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
import spacy
import fitz 
import re
import os
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.contrib import messages
import re 

from django.contrib.auth import authenticate, login, logout


def log_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')
            return render(request, 'login.html')
    return render(request, 'login.html')

def register(request):
    
    name = request.POST.get('name')
    pass1 = request.POST.get('pass1')
    pass2 = request.POST.get('pass2')
    email = request.POST.get('email')
    first = request.POST.get('first')
    last = request.POST.get('last')
    
    if request.method == 'POST':
        if pass1 == pass2:
            if User.objects.filter(email = email).exists():
                messages.error(request,'email already there')
                return render(request,'register.html')
            else:
                user = User.objects.create_user(
                    username = name,
                    password = pass2,
                    email = email,
                    first_name = first,
                    last_name = last
                )
                user.save()
                return redirect('login')
        else:
            messages.error(request,'mismatch password')
            return render(request,'register.html')
            
    return render(request,'register.html')

def log_out(request):
    logout(request)
    return redirect('login')

def clean_text(text):
    """
    Clean the input text by removing unwanted characters and normalizing spaces.
    """
    # Replace non-ASCII characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Replace specific special characters with spaces
    text = re.sub(r'[\_\*\•\·\-\–\—\~]+', ' ', text)
    
    # Replace newlines with a space
    text = text.replace('\n', ' ')

    # Replace multiple spaces with a single space
    text = re.sub(r'[ ]+', ' ', text)

    # Normalize spaces and preserve newlines
    text = "\n".join(line.strip() for line in text.splitlines())

    return text

def home(request):
    """
    Handles PDF uploads, extracts and cleans text, and processes entities with spaCy.
    """
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']

        # Save the uploaded file
        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)

        # Load the trained spaCy model dynamically
        model_path = os.path.join(settings.BASE_DIR, 'app1', 'team_model')  # Adjust path as needed
        try:
            nlp = spacy.load(model_path)
        except Exception as e:
            messages.error(request, f"Error loading spaCy model: {str(e)}")
            return redirect('home')

        # Initialize dictionary to store extracted entities
        extracted_data = {
            'persons': set(),
            'phone_numbers': set(),
            'emails': set(),
            'skills': set(),
            'designations': [],  # Keep as list if ordering matters
            'organizations': [],  # Keep as list if ordering matters
            'dates': [],  # Keep as list if ordering matters
            'educations': [],  # Keep as list if ordering matters
            'institutes': [],  # Keep as list if ordering matters
            'date_of_birth': set(),
        }

        # Email validation regex pattern
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

        # Phone number regex pattern (example for Indian phone numbers)
        phone_pattern = re.compile(
            r"""
            (?:\+91[\s-]?)?          # Optional country code +91 with or without space/dash
            (?:91[\s-]?)?            # Optional country code 91 with or without space/dash
            [6-9]\d{9}               # Starts with 6, 7, 8, or 9 and followed by 9 digits
            """, 
            re.VERBOSE
        )

        try:
            # Extract text from the uploaded PDF using fitz
            doc_text = ""
            with fitz.open(file_path) as pdf:
                for page in pdf:
                    text = page.get_text()  # Extract text from each page
                    doc_text += text

            # Clean the extracted text
            cleaned_text = clean_text(doc_text)

            # Process the cleaned text with spaCy
            if cleaned_text:
                doc = nlp(cleaned_text)
                
                # Process each entity extracted by spaCy
                for ent in doc.ents:
                    print(f"{ent.label_} - {ent.text}")  # Print entities to the console
                    if ent.label_ == "PERSON":
                        extracted_data['persons'].add(ent.text)
                    elif ent.label_ == "PHONE":
                        extracted_data['phone_numbers'].add(ent.text)
                    elif ent.label_ == "EMAIL":
                        if email_pattern.match(ent.text):  # Validate email
                            extracted_data['emails'].add(ent.text)
                    elif ent.label_ == "SKILL":
                        extracted_data['skills'].add(ent.text)
                    elif ent.label_ == "DATE_OF_BIRTH":
                        extracted_data['date_of_birth'].add(ent.text)
                    elif ent.label_ == "DESIGNATION":
                        extracted_data['designations'].append(ent.text)
                    elif ent.label_ == "ORG":
                        extracted_data['organizations'].append(ent.text)
                    elif ent.label_ == "DATE":
                        extracted_data['dates'].append(ent.text)
                    elif ent.label_ == "EDUCATION":
                        extracted_data['educations'].append(ent.text)
                    elif ent.label_ == "INSTITUTE":
                        extracted_data['institutes'].append(ent.text)

                # Fallback for phone numbers if not detected by spaCy
                if not extracted_data['phone_numbers']:
                    phone_matches = phone_pattern.findall(doc_text)
                    extracted_data['phone_numbers'].update(phone_matches)

            # Convert sets back to lists for database storage
            Entity.objects.create(
                persons=list(extracted_data['persons']),
                phone_numbers=list(extracted_data['phone_numbers']),
                emails=list(extracted_data['emails']),
                skills=list(extracted_data['skills']),
                designations=extracted_data['designations'],
                organizations=extracted_data['organizations'],
                dates=extracted_data['dates'],
                educations=extracted_data['educations'],
                institutes=extracted_data['institutes'],
                date_of_birth=list(extracted_data['date_of_birth']),
            )

            messages.success(request, "File processed and data saved successfully!")
        except Exception as e:
            messages.error(request, f"Error processing file: {str(e)}")
            return redirect('home')

        return redirect('home')

    return render(request, 'home.html',{'page_obj': Entity.objects.all()})

def user_details(request, entity_id):
    
    entity = get_object_or_404(Entity, id=entity_id)
    
    if request.method == 'POST':
        id = request.POST.get('delete')
        a = Entity.objects.get(id = id)
        a.delete()
        return redirect('home')

    return render(request, 'user_details.html', {'entity': entity})