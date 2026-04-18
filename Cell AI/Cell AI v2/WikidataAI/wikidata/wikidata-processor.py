import json
import os
import argparse
import requests
import gzip
import logging
import re
import time
import multiprocessing
from tqdm import tqdm
from collections import defaultdict
from functools import partial
import tempfile
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('AdvancedWikidataProcessor')

# Dictionary mapping Wikidata property IDs to human-readable names
PROPERTIES = {
    # Common properties
    "P31": "instance of",
    "P279": "subclass of",
    "P1343": "described by source",
    "P5185": "Wikidata property",
    "P5238": "represented by",
    "P5275": "Wikidata lexeme ID",
    "P5191": "grammatical features",
    "P5920": "described by source",
    "P6140": "Wikisaurus ID",
    "P9529": "Wikisaurus ID",
    "P10831": "identified by",
    "P12510": "OpenRefine ID",
    "P12573": "lexical category",
    "P12690": "dictionary entry ID",
    "P12718": "dictionary language code",
    "P12724": "word class code",
    "P12726": "sense ID",
    "P12739": "definition",
    "P12828": "LexSem ID",
    "P5912": "lexical concept",
    "P9962": "Lexemes.org ID",
    "P11138": "dictionary ID",
    "P11481": "entry code",
    "P13258": "lexeme database ID",
    "P13163": "dictionary search key",
    "P11328": "refers to form",
    "P5402": "lexical translation",
    "P12675": "form number",
    "P12448": "SIL lexeme ID",
    "P12868": "homograph number",
    "P460": "said to be the same as",
    "P1269": "facet of",
    "P361": "part of",
    "P397": "parent body",
    "P398": "child body",
    
    # Linguistic properties
    "P407": "language",
    "P10339": "grammatical gender",
    "P5944": "grammatical number",
    "P5940": "grammatical case",
    "P5946": "grammatical tense",
    "P5941": "grammatical mood",
    "P5942": "grammatical person",
    "P5943": "grammatical voice",
    "P425": "field of study",
    "P138": "named after",
    "P1552": "has quality",
    "P1535": "used by",
    "P5137": "item for this lexeme",
    "P10689": "grammatical agreement",
    "P7506": "pragmatics",
    "P7287": "etymology",
    "P642": "of",
    "P552": "handedness",
    "P2670": "has parts of the class",
    
    # Identifier properties
    "P646": "Freebase ID",
    "P1014": "BabelNet ID",
    "P18": "image",
    "P1323": "gallica ID",
    "P3417": "Quora topic ID",
    "P1417": "Britannica ID",
    "P227": "GND ID",
    "P214": "VIAF ID",
    "P1566": "GeoNames ID",
    "P1245": "OmegaWiki ID",
    "P373": "Commons category",
    "P910": "main category",
    "P1419": "shape",
    "P3219": "BNCF ID",
    "P244": "Library of Congress ID",
    "P3782": "Dictionary ID",
    "P3986": "Dictionary headword",
    "P3987": "Dictionary definition",
    "P4919": "PanLex ID",
    "P8814": "FrameNet ID",
    
    # Other common properties
    "P1889": "different from",
    "P3342": "significant event",
    "P2283": "uses",
    "P366": "has use",
    "P2670": "has parts of the class",
    "P527": "has part",
    "P2670": "has parts of the class",
    "P1535": "used by",
    "P2079": "fabrication method"
}

# Dictionary mapping common entity IDs to human-readable names
ENTITIES = {
    # Languages
    "Q1860": "English",
    "Q188": "German",
    "Q150": "French",
    "Q131": "Spanish",
    "Q13955": "Italian",
    "Q7737": "Russian",
    "Q9292": "Chinese",
    "Q5287": "Portuguese",
    "Q9610": "Japanese",
    "Q9035": "Korean",
    "Q8748": "Arabic",
    "Q5885": "Hebrew",
    "Q36236": "Polish",
    "Q9067": "Dutch",
    "Q9072": "Turkish",
    "Q9083": "Swedish",
    "Q29": "Spanish",
    "Q652": "Italian",
    "Q7850": "Russian",
    "Q9176": "Chinese",
    
    # Parts of speech
    "Q1084": "noun",
    "Q24905": "verb",
    "Q36224": "adjective",
    "Q4149": "pronoun",
    "Q9292": "adverb",
    "Q162940": "preposition",
    "Q10616": "conjunction",
    "Q103184": "interjection",
    "Q147276": "determiner",
    "Q10389": "word",
    "Q1520022": "lexical item",
    "Q1520033": "lexeme",
    "Q1350145": "noun",
    "Q24905": "verb",
    "Q34698": "part of speech",
    "Q164509": "suffix",
    "Q102047": "prefix",
    "Q134830": "affix",
    "Q125661": "infix",
    "Q62155": "transitive verb",
    "Q179639": "intransitive verb",
    "Q682111": "common noun",
    "Q61053035": "countable noun",
    "Q2865743": "uncountable noun",
    "Q110786": "collective noun",
    "Q130901": "concrete noun",
    "Q163649": "abstract noun",
    "Q185155": "proper noun",
    "Q208683": "mass noun",
    "Q2865743": "uncountable noun",
    
    # Grammatical features
    "Q146786": "singular",
    "Q146786": "plural",
    "Q499327": "masculine",
    "Q1775415": "feminine",
    "Q1305037": "neuter",
    "Q185077": "past tense",
    "Q192613": "present tense",
    "Q3910936": "future tense",
    "Q179230": "nominative case",
    "Q146233": "genitive case",
    "Q145599": "dative case",
    "Q146078": "accusative case",
    "Q185072": "subjunctive mood",
    "Q179290": "indicative mood",
    "Q52434162": "imperative mood",
    
    # Linguistic concepts
    "Q8142": "language",
    "Q1840": "grammar",
    "Q9779": "linguistics",
    "Q36013": "syntax",
    "Q190492": "semantics",
    "Q28563": "phonology",
    "Q145292": "morphology",
    "Q10389": "word",
    "Q860906": "sentence",
    "Q1221939": "phrase",
    "Q10387": "meaning",
    "Q9357": "synonym",
    "Q8445": "antonym",
    "Q61476": "homonym",
    "Q42889": "vocabulary",
    "Q43013": "dialect",
    "Q571": "book",
    "Q33215": "dictionary",
    "Q8242": "essay",
    "Q28389": "thesaurus",
    "Q10391": "speech",
    "Q2398963": "homograph",
    
    # General concepts
    "Q1979154": "information",
    "Q11660": "knowledge",
    "Q8366": "work",
    "Q121769": "algorithm",
    "Q166247": "knowledge representation",
    "Q172847": "machine learning",
    "Q151885": "policy",
    "Q9071": "time",
    "Q35120": "entity",
    "Q15978631": "person",
    "Q8436": "mammal",
    "Q11563": "number",
    "Q5": "human",
    "Q3504248": "planet",
    "Q544": "Solar System",
    "Q313": "Sun",
    "Q2": "Earth",
    "Q7725634": "artificial intelligence"
}

# Dictionary mapping grammatical features to human-readable descriptions
GRAMMATICAL_FEATURES = {
    # Tense
    "L42605": "present",
    "L36823": "past",
    "L268592": "infinitive",
    "L329263": "imperative",
    "L333957": "first-person",
    "L334124": "second-person",
    "L330480": "third-person",
    "L4699": "singular",
    "L618779": "plural"
}

# Extract meanings from property-value combinations
PROPERTY_VALUE_MEANINGS = {
    "P31:Q1520033": "a lexeme",
    "P31:Q1350145": "a noun",
    "P31:Q24905": "a verb",
    "P31:Q36224": "an adjective",
    "P31:Q4149": "a pronoun",
    "P31:Q9292": "an adverb",
    "P31:Q162940": "a preposition",
    "P31:Q10616": "a conjunction",
    "P31:Q103184": "an interjection",
    "P31:Q147276": "a determiner",
    "P31:Q61053035": "a countable noun",
    "P31:Q2865743": "an uncountable noun",
    "P31:Q110786": "a collective noun",
    "P31:Q682111": "a common noun",
    "P31:Q185155": "a proper noun",
    "P31:Q5": "a human",
    "P31:Q8436": "a mammal",
    "P31:Q3504248": "a planet"
}

# Dictionary of available Wikidata dumps
WIKIDATA_DUMPS = {
    "all": {
        "name": "Complete Entities",
        "description": "Complete Wikidata entities dump (very large, ~100GB compressed)",
        "url": "https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.gz"
    },
    "lexemes": {
        "name": "Lexemes Only",
        "description": "Wikidata lexemes dump (smaller subset)",
        "url": "https://dumps.wikimedia.org/wikidatawiki/entities/latest-lexemes.json.gz"
    },
    "truthy": {
        "name": "Truthy Statements",
        "description": "Only the current truthy statements dump",
        "url": "https://dumps.wikimedia.org/wikidatawiki/entities/latest-truthy.nt.gz"
    },
    "properties": {
        "name": "Properties",
        "description": "Properties dump with definitions and labels",
        "url": "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=P6|P11&props=info|datatype|labels|descriptions|aliases&format=json"
    }
}

def list_available_dumps():
    """
    Display a list of available Wikidata dumps
    """
    logger.info("Available Wikidata dumps:")
    for dump_id, dump_info in WIKIDATA_DUMPS.items():
        logger.info(f"  - {dump_id}: {dump_info['name']} - {dump_info['description']}")

def download_wikidata_dump(output_dir='./wikidata_dumps', dump_type='lexemes', dump_url=None):
    """
    Download the specified Wikidata dump or use provided URL
    
    Args:
        output_dir: Directory to save the downloaded dump
        dump_type: Type of dump to download (all, lexemes, truthy, properties)
        dump_url: Custom URL to download from (overrides dump_type)
    
    Returns:
        Path to the downloaded file
    """
    os.makedirs(output_dir, exist_ok=True)
    
    if dump_url is None:
        if dump_type not in WIKIDATA_DUMPS:
            logger.error(f"Unknown dump type: {dump_type}")
            logger.info("Available dump types:")
            for dtype in WIKIDATA_DUMPS:
                logger.info(f"  - {dtype}: {WIKIDATA_DUMPS[dtype]['name']}")
            raise ValueError(f"Unknown dump type: {dump_type}")
        
        dump_url = WIKIDATA_DUMPS[dump_type]['url']
        logger.info(f"Selected {WIKIDATA_DUMPS[dump_type]['name']} dump")
    
    output_path = os.path.join(output_dir, os.path.basename(dump_url))
    
    if os.path.exists(output_path):
        logger.info(f"Dump file already exists at {output_path}, skipping download")
        return output_path
    
    logger.info(f"Downloading Wikidata dump from {dump_url}")
    
    # Download with progress bar
    try:
        response = requests.get(dump_url, stream=True, timeout=300)  # Increased timeout for large files
        response.raise_for_status()  # Raise exception for bad responses
        
        # Check content type
        content_type = response.headers.get('content-type', '')
        is_json = 'json' in content_type.lower()
        is_gzip = 'gzip' in content_type.lower() or dump_url.endswith('.gz')
        
        if not (is_json or is_gzip):
            logger.warning(f"Warning: Downloaded file may not be in expected format. Content-Type: {content_type}")
        
        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 1024*1024  # 1MB chunks
        
        with open(output_path, 'wb') as f:
            with tqdm(
                total=total_size // chunk_size if total_size else None, 
                unit='MB',
                desc=f"Downloading {os.path.basename(dump_url)}"
            ) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(1)
        
        # Verify the downloaded file
        if is_gzip:
            try:
                with gzip.open(output_path, 'rb') as test:
                    test.read(2)  # Just read a tiny bit to verify format
                logger.info(f"Successfully downloaded Wikidata dump to {output_path}")
            except gzip.BadGzipFile:
                logger.error(f"Downloaded file is not a valid gzip file. Please check the URL.")
                os.remove(output_path)  # Remove the invalid file
                raise ValueError("Downloaded file is not a valid gzip file")
        else:
            # For JSON files, just check if it's valid
            file_size = os.path.getsize(output_path)
            if file_size < 10:  # Extremely small file is suspicious
                logger.error(f"Downloaded file is suspiciously small ({file_size} bytes). Please check the URL.")
                os.remove(output_path)
                raise ValueError("Downloaded file is suspiciously small")
            logger.info(f"Successfully downloaded Wikidata dump to {output_path}")
                
        return output_path
            
    except requests.RequestException as e:
        logger.error(f"Error downloading file: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)  # Remove partial download
        raise

def categorize_facts(facts):
    """
    Categorize facts into different categories for better organization
    """
    categories = {
        "definition": [],
        "grammatical": [],
        "linguistic": [],
        "external_ids": [],
        "semantic": [],
        "other": []
    }
    
    for fact in facts:
        fact = fact.strip()
        if not fact.startswith('- '):
            categories["other"].append(fact)
            continue
            
        # Check categories based on content
        fact_lower = fact.lower()
        
        # Definitions and descriptions
        if any(term in fact_lower for term in ['definition', 'description', 'meaning']):
            categories["definition"].append(fact)
        
        # Grammatical features
        elif any(term in fact_lower for term in ['grammatical', 'tense', 'mood', 'voice', 'number', 'gender', 'person', 'case']):
            categories["grammatical"].append(fact)
        
        # Linguistic categorization
        elif any(term in fact_lower for term in ['instance of', 'lexical', 'language', 'part of speech', 'noun', 'verb', 'adjective']):
            categories["linguistic"].append(fact)
            
        # External IDs and references
        elif any(term in fact_lower for term in ['id', 'identifier', 'database', 'dictionary', 'code', 'wikisaurus', 'lexemes.org']):
            categories["external_ids"].append(fact)
            
        # Semantic relationships
        elif any(term in fact_lower for term in ['represented by', 'refers to', 'translation', 'synonym', 'antonym', 'related']):
            categories["semantic"].append(fact)
            
        # Other
        else:
            categories["other"].append(fact)
    
    return categories

def extract_definitions(facts):
    """
    Try to extract definitions from facts
    """
    definitions = []
    
    # Look specifically for dictionary definitions
    for fact in facts:
        # Look for dictionary definition
        if "definition:" in fact.lower():
            def_match = re.search(r'definition: (.+)', fact, re.IGNORECASE)
            if def_match:
                definitions.append(def_match.group(1))
        
        # Look for dictionary meaning
        elif "meaning:" in fact.lower():
            meaning_match = re.search(r'meaning: (.+)', fact, re.IGNORECASE)
            if meaning_match:
                definitions.append(meaning_match.group(1))
                
        # Look for description
        elif "description:" in fact.lower():
            desc_match = re.search(r'description: (.+)', fact, re.IGNORECASE)
            if desc_match:
                definitions.append(desc_match.group(1))
    
    return definitions

def extract_word_info(facts):
    """
    Extract detailed linguistic information from facts
    """
    info = {
        "pos": None,
        "language": None,
        "grammatical_features": [],
        "is_countable": None
    }
    
    for fact in facts:
        # Extract part of speech
        if "instance of: noun" in fact.lower() or "instance of: a noun" in fact.lower():
            info["pos"] = "noun"
        elif "instance of: verb" in fact.lower() or "instance of: a verb" in fact.lower():
            info["pos"] = "verb"
        elif "instance of: adjective" in fact.lower() or "instance of: an adjective" in fact.lower():
            info["pos"] = "adjective"
        elif "instance of: adverb" in fact.lower():
            info["pos"] = "adverb"
        elif "instance of: pronoun" in fact.lower():
            info["pos"] = "pronoun"
        elif "instance of: preposition" in fact.lower():
            info["pos"] = "preposition"
        elif "instance of: conjunction" in fact.lower():
            info["pos"] = "conjunction"
        elif "instance of: interjection" in fact.lower():
            info["pos"] = "interjection"
        
        # Extract language information
        for lang in ["English", "German", "French", "Spanish", "Italian", "Russian", "Chinese", "Japanese"]:
            if f"language: {lang}" in fact:
                info["language"] = lang
                break
        
        # Look for countability information
        if "countable noun" in fact.lower():
            info["is_countable"] = True
        elif "uncountable noun" in fact.lower() or "mass noun" in fact.lower():
            info["is_countable"] = False
        
        # Extract grammatical features
        for feature in ["singular", "plural", "masculine", "feminine", "neuter", "past tense", 
                      "present tense", "future tense", "imperative", "subjunctive", "indicative"]:
            if feature in fact.lower():
                info["grammatical_features"].append(feature)
        
        # Extract lexeme features from entity IDs
        for feature_id, feature_name in GRAMMATICAL_FEATURES.items():
            if feature_id in fact:
                info["grammatical_features"].append(feature_name)
    
    return info

def enhance_fact_line(line):
    """
    Transform a fact line from "- P123: Q456" format to something more readable
    """
    # Skip lines that don't match the expected pattern
    if not line.startswith('- P'):
        return line
    
    # Extract the property ID and value
    match = re.match(r'- (P\d+)(?:\s*\([^)]+\))?: (.+)', line)
    if not match:
        return line
        
    prop_id, value = match.groups()
    
    # Check if we already have a property label in the line
    if f"({PROPERTIES.get(prop_id, prop_id)})" in line:
        # Skip further processing if property is already labeled
        pass
    else:
        # Get the property label
        prop_label = PROPERTIES.get(prop_id, prop_id)
        line = f"- {prop_label} ({prop_id}): {value}"
    
    # Check if the value is a Wikidata entity (Q or L)
    entity_match = re.match(r'([QL]\d+)$', value.strip())
    if entity_match:
        entity_id = entity_match.group(1)
        entity_label = ENTITIES.get(entity_id, entity_id)
        
        # Format differently depending on whether we have a human-readable label
        if entity_id != entity_label:
            return f"- {prop_label} ({prop_id}): {entity_label} ({entity_id})"
        else:
            return f"- {prop_label} ({prop_id}): {entity_id}"
    
    # Check for property:value meaning
    prop_value_key = f"{prop_id}:{value.strip()}"
    if prop_value_key in PROPERTY_VALUE_MEANINGS:
        meaning = PROPERTY_VALUE_MEANINGS[prop_value_key]
        return f"- {prop_label} ({prop_id}): {value} (This means it's {meaning})"
    
    return line

def derive_title(entity_id, facts):
    """
    Try to derive a meaningful title from the entity ID and facts
    """
    # For lexemes, try to find a word form
    title = None
    
    # First check for title in facts
    for fact in facts:
        if fact.lower().startswith("title:"):
            title_match = re.search(r'title: (.+)', fact, re.IGNORECASE)
            if title_match:
                return title_match.group(1)
    
    if entity_id.startswith('L'):
        # Check for dictionary headword
        for fact in facts:
            if "dictionary headword:" in fact.lower():
                match = re.search(r'dictionary headword: (.+)', fact, re.IGNORECASE)
                if match:
                    return match.group(1)
            
            # Check for dictionary entry
            elif "dictionary entry:" in fact.lower():
                match = re.search(r'dictionary entry: (.+)', fact, re.IGNORECASE)
                if match:
                    return match.group(1)
    
    # If no title found, use entity ID or known label
    if entity_id.startswith('Q'):
        return ENTITIES.get(entity_id, f"Concept {entity_id}")
    else:
        return f"Word {entity_id}"

def extract_claims_from_raw_entity(entity, language='en'):
    """
    Extract claims from a raw Wikidata entity in a structured format
    """
    facts = []
    
    # Process claims if they exist
    if 'claims' in entity:
        for prop_id, claim_group in entity['claims'].items():
            for claim in claim_group:
                if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                    prop_name = PROPERTIES.get(prop_id, prop_id)
                    
                    if 'datavalue' in claim['mainsnak']:
                        datavalue = claim['mainsnak']['datavalue']
                        
                        if 'value' in datavalue:
                            value = datavalue['value']
                            
                            # Handle different value types
                            if isinstance(value, dict):
                                if 'id' in value:  # Entity reference
                                    entity_id = value['id']
                                    entity_label = ENTITIES.get(entity_id, entity_id)
                                    facts.append(f"- {prop_id}: {entity_id}")
                                elif 'text' in value and 'language' in value:  # Monolingual text
                                    # Include text in all languages, but mark the language
                                    facts.append(f"- {prop_id}: {value['text']} ({value['language']})")
                            elif isinstance(value, str):
                                facts.append(f"- {prop_id}: {value}")
                            elif isinstance(value, (int, float)):
                                facts.append(f"- {prop_id}: {value}")
    
    return facts

def extract_senses_from_lexeme(entity, language='en'):
    """
    Extract senses from a lexeme entity
    """
    facts = []
    
    if 'senses' in entity:
        for i, sense in enumerate(entity['senses']):
            sense_id = sense.get('id', f"Sense {i+1}")
            
            # Extract glosses (definitions)
            if 'glosses' in sense:
                # Try preferred language first
                if language in sense['glosses'] and 'value' in sense['glosses'][language]:
                    facts.append(f"- definition: {sense['glosses'][language]['value']} (Sense {i+1})")
                # If not available, include definitions from other languages with language tag
                else:
                    for lang, gloss in sense['glosses'].items():
                        if 'value' in gloss:
                            facts.append(f"- definition: {gloss['value']} ({lang}, Sense {i+1})")
            
            # Extract sense claims
            if 'claims' in sense:
                for prop_id, claims in sense['claims'].items():
                    for claim in claims:
                        if 'mainsnak' in claim and 'datavalue' in claim['mainsnak']:
                            datavalue = claim['mainsnak']['datavalue']
                            if 'value' in datavalue:
                                value = datavalue['value']
                                if isinstance(value, dict) and 'id' in value:
                                    facts.append(f"- {prop_id}: {value['id']} (Sense {i+1})")
                                elif isinstance(value, str):
                                    facts.append(f"- {prop_id}: {value} (Sense {i+1})")
    
    return facts

def extract_forms_from_lexeme(entity, language='en'):
    """
    Extract forms from a lexeme entity
    """
    facts = []
    
    if 'forms' in entity:
        for i, form in enumerate(entity['forms']):
            form_id = form.get('id', f"Form {i+1}")
            
            # Extract the actual word form
            if 'representations' in form:
                # Try to get representation in preferred language first
                if language in form['representations'] and 'value' in form['representations'][language]:
                    facts.append(f"- word form: {form['representations'][language]['value']} (Form {i+1})")
                # Include all representations with language tags
                else:
                    for lang, representation in form['representations'].items():
                        if 'value' in representation:
                            facts.append(f"- word form: {representation['value']} ({lang}, Form {i+1})")
            
            # Extract grammatical features
            if 'grammaticalFeatures' in form:
                features = []
                for feature_id in form['grammaticalFeatures']:
                    feature_name = GRAMMATICAL_FEATURES.get(feature_id, feature_id)
                    features.append(feature_name)
                
                if features:
                    facts.append(f"- grammatical features: {', '.join(features)} (Form {i+1})")
    
    return facts

def process_raw_wikidata_entity(entity, language='en'):
    """
    Process a raw Wikidata entity into a structured text format
    """
    entity_id = entity.get('id', '')
    is_lexeme = entity_id.startswith('L')
    text = ""
    
    # Extract label/lemma - lexemes use 'lemmas' instead of 'labels'
    label = None
    if is_lexeme and 'lemmas' in entity:
        # Try to get lemma in the preferred language first
        if language in entity['lemmas']:
            label = entity['lemmas'][language]['value']
            text += f"Title: {label}\n"
        # If not available, get the first available lemma
        elif entity['lemmas']:
            first_lang = next(iter(entity['lemmas']))
            label = entity['lemmas'][first_lang]['value']
            text += f"Title: {label} ({first_lang})\n"
    elif 'labels' in entity:
        # Try to get label in the preferred language first
        if language in entity['labels']:
            label = entity['labels'][language]['value']
            text += f"Title: {label}\n"
        # If not available, get the first available label
        elif entity['labels']:
            first_lang = next(iter(entity['labels']))
            label = entity['labels'][first_lang]['value']
            text += f"Title: {label} ({first_lang})\n"
    
    # Extract description - try preferred language first, then any language
    description = None
    if 'descriptions' in entity:
        if language in entity['descriptions']:
            description = entity['descriptions'][language]['value']
            text += f"Description: {description}\n"
        elif entity['descriptions']:
            first_lang = next(iter(entity['descriptions']))
            description = entity['descriptions'][first_lang]['value']
            text += f"Description: {description} ({first_lang})\n"
    
    # Extract aliases - try preferred language first, then any language
    aliases = []
    if 'aliases' in entity:
        if language in entity['aliases']:
            aliases = [alias['value'] for alias in entity['aliases'][language]]
            if aliases:
                text += f"Also known as: {', '.join(aliases)}\n"
        elif entity['aliases']:
            first_lang = next(iter(entity['aliases']))
            aliases = [alias['value'] for alias in entity['aliases'][first_lang]]
            if aliases:
                text += f"Also known as: {', '.join(aliases)} ({first_lang})\n"
    
    # Extract lexical category for lexemes
    if is_lexeme and 'lexicalCategory' in entity:
        category_id = entity['lexicalCategory']
        category_name = ENTITIES.get(category_id, category_id)
        text += f"Part of speech: {category_name} ({category_id})\n"
    
    # Extract language for lexemes
    if is_lexeme and 'language' in entity:
        lang_id = entity['language']
        lang_name = ENTITIES.get(lang_id, lang_id)
        text += f"Language: {lang_name} ({lang_id})\n"
    
    # Extract claims
    claims = extract_claims_from_raw_entity(entity, language)
    
    # For lexemes, also extract forms and senses
    if is_lexeme:
        forms = extract_forms_from_lexeme(entity, language)
        senses = extract_senses_from_lexeme(entity, language)
        
        if forms:
            claims.extend(forms)
        if senses:
            claims.extend(senses)
    
    if claims:
        text += "Facts:\n"
        for claim in claims:
            text += f"{claim}\n"
    
    # Return the processed entry
    return {
        'id': entity_id,
        'text': text.strip()
    }

def format_entry(entry):
    """
    Format a Wikidata entry into a much more readable and informative form
    """
    if 'id' not in entry or 'text' not in entry:
        return entry
    
    entity_id = entry['id']
    text = entry['text']
    is_lexeme = entity_id.startswith('L')
    
    # Split facts section if it exists
    facts_section = ""
    header_section = text
    facts = []
    
    if 'Facts:' in text:
        parts = text.split('Facts:', 1)
        header_section = parts[0].strip()
        facts_section = parts[1].strip()
        facts = [line.strip() for line in facts_section.split('\n') if line.strip()]
    
    # Process each fact for better readability
    enhanced_facts = [enhance_fact_line(fact) for fact in facts]
    
    # Add header section items as facts for processing
    for line in header_section.split('\n'):
        if line.strip():
            enhanced_facts.append(line.strip())
    
    # Categorize facts
    categorized_facts = categorize_facts(enhanced_facts)
    
    # Extract definitions if available
    definitions = extract_definitions(enhanced_facts)
    
    # Extract linguistic information
    word_info = extract_word_info(enhanced_facts)
    
    # Try to derive a meaningful title
    title = derive_title(entity_id, enhanced_facts)
    
    # Build a rich, structured entry
    new_text = ""
    
    # Add title
    if is_lexeme:
        new_text += f"Word: {title}\n\n"
    else:
        new_text += f"Concept: {title}\n\n"
    
    # Add linguistic information for lexemes
    if is_lexeme:
        # Add part of speech and language
        linguistic_parts = []
        if word_info["language"]:
            linguistic_parts.append(f"{word_info['language']} word")
        if word_info["pos"]:
            pos_desc = word_info["pos"]
            if word_info["pos"] == "noun" and word_info["is_countable"] is not None:
                pos_desc = "countable noun" if word_info["is_countable"] else "uncountable noun"
            linguistic_parts.append(pos_desc)
            
        if linguistic_parts:
            new_text += f"Type: {', '.join(linguistic_parts)}\n\n"
        
        # Add grammatical features
        if word_info["grammatical_features"]:
            new_text += f"Grammatical features: {', '.join(word_info['grammatical_features'])}\n\n"
    
    # Add definitions if found
    if definitions:
        new_text += "Definitions:\n"
        for i, definition in enumerate(definitions):
            new_text += f"{i+1}. {definition}\n"
        new_text += "\n"
    
    # Add categorized facts
    # First linguistic information
    if categorized_facts["linguistic"]:
        new_text += "Linguistic Classification:\n"
        for fact in categorized_facts["linguistic"]:
            new_text += f"{fact}\n"
        new_text += "\n"
    
    # Then grammatical information
    if categorized_facts["grammatical"]:
        new_text += "Grammatical Information:\n"
        for fact in categorized_facts["grammatical"]:
            new_text += f"{fact}\n"
        new_text += "\n"
    
    # Then semantic relationships
    if categorized_facts["semantic"]:
        new_text += "Semantic Relationships:\n"
        for fact in categorized_facts["semantic"]:
            new_text += f"{fact}\n"
        new_text += "\n"
    
    # Add other non-ID facts
    other_facts = categorized_facts["other"]
    if other_facts:
        new_text += "Other Information:\n"
        for fact in other_facts:
            new_text += f"{fact}\n"
        new_text += "\n"
    
    # Finally add external IDs (often less important for chatbot)
    if categorized_facts["external_ids"]:
        new_text += "External Identifiers:\n"
        for fact in categorized_facts["external_ids"]:
            new_text += f"{fact}\n"
        new_text += "\n"
    
    # Return updated entry
    return {
        'id': entity_id,
        'text': new_text.strip()
    }

def get_line_offsets(file_path, sample_size=1000):
    """
    Get approximate line offsets for a gzipped file by sampling
    """
    logger.info(f"Scanning file to determine chunk sizes...")
    
    total_size = os.path.getsize(file_path)
    
    # Quick scan to estimate total lines
    with gzip.open(file_path, 'rt', encoding='utf-8') as f:
        # Read sample lines to estimate average line size
        sample_lines = []
        for _ in range(sample_size):
            line = f.readline()
            if not line:
                break
            sample_lines.append(line)
        
        # If we didn't get enough lines, adjust
        if len(sample_lines) < sample_size:
            logger.warning(f"File has fewer than {sample_size} lines, adjusting...")
            sample_size = len(sample_lines)
            
        if sample_size == 0:
            logger.error("Could not read any lines from the file")
            return []
        
        # Calculate average line size based on the sample
        avg_line_size = sum(len(line) for line in sample_lines) / sample_size
        
        # Estimate total lines
        estimated_total_lines = int(total_size / avg_line_size * 0.7)  # Compression factor approximation
        logger.info(f"Estimated total lines: {estimated_total_lines}")
        
        return estimated_total_lines

def find_chunk_boundaries(dump_path, num_chunks):
    """
    Find chunk boundaries for parallel processing
    """
    estimated_lines = get_line_offsets(dump_path)
    
    # Safety check
    if estimated_lines <= 0:
        logger.warning("Could not estimate line count, defaulting to 1 chunk")
        return [0]
    
    # Calculate lines per chunk
    lines_per_chunk = max(1, estimated_lines // num_chunks)
    
    # Create chunk boundaries
    boundaries = []
    for i in range(0, num_chunks):
        boundaries.append(i * lines_per_chunk)
    
    logger.info(f"Created {len(boundaries)} chunk boundaries: {boundaries[:5]}... (lines per chunk: {lines_per_chunk})")
    return boundaries

def process_chunk(dump_path, output_path, start_line, chunk_size, max_items_per_chunk, language='en'):
    """
    Process a chunk of the Wikidata dump file
    """
    processed_count = 0
    total_count = 0
    chunk_id = os.path.basename(output_path)
    
    try:
        with gzip.open(dump_path, 'rt', encoding='utf-8') as f_in:
            with open(output_path, 'w', encoding='utf-8') as f_out:
                # Skip to start line
                for _ in range(start_line):
                    if not f_in.readline():
                        logger.warning(f"Chunk {chunk_id}: Reached EOF before start line {start_line}")
                        return processed_count
                
                # Process a finite number of lines for the chunk, or until EOF
                lines_processed = 0
                while lines_processed < chunk_size or chunk_size == float('inf'):
                    line = f_in.readline()
                    if not line:  # EOF
                        break
                    
                    if chunk_size != float('inf'):
                        lines_processed += 1
                    total_count += 1
                
                    # Clean the line
                    line = line.strip()
                    if line.endswith(','):
                        line = line[:-1]
                    
                    # Skip empty lines or closing bracket
                    if not line or line == ']':
                        continue
                    
                    try:
                        # Parse the raw JSON entity
                        entity = json.loads(line)
                        entity_id = entity.get('id', '')
                        
                        # Check if it's a lexeme (starts with L)
                        is_lexeme = entity_id.startswith('L')
                        
                        # Process all entities regardless of language
                        # Just make sure they have some basic structure
                        if is_lexeme and 'lemmas' not in entity:
                            continue
                        if not is_lexeme and 'labels' not in entity:
                            continue
                        
                        # Process the raw entity into initial text format
                        processed_entry = process_raw_wikidata_entity(entity, language)
                        
                        # Format the entry with enhanced formatting
                        enhanced_entry = format_entry(processed_entry)
                        
                        # Write the enhanced entry
                        f_out.write(json.dumps(enhanced_entry) + '\n')
                        processed_count += 1
                        
                        if processed_count >= max_items_per_chunk:
                            logger.info(f"Chunk {chunk_id}: Reached max items limit ({max_items_per_chunk})")
                            break
                        
                    except json.JSONDecodeError:
                        continue
                    except Exception as e:
                        continue
    
    except Exception as e:
        logger.error(f"Error in chunk {chunk_id}: {e}")
    
    logger.info(f"Chunk {chunk_id}: Processed {processed_count} entities from {total_count} lines")
    return processed_count

def merge_output_files(temp_files, output_path):
    """
    Merge temporary output files into the final output file
    """
    with open(output_path, 'w', encoding='utf-8') as outfile:
        for temp_file in temp_files:
            if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                with open(temp_file, 'r', encoding='utf-8') as infile:
                    shutil.copyfileobj(infile, outfile)
                    
def process_wikidata_dump_parallel(dump_path, output_path, max_items=None, language='en', num_processes=None):
    """
    Process Wikidata JSON dump in parallel using multiple processes
    
    Args:
        dump_path: Path to the Wikidata dump file (.json.gz)
        output_path: Path to save the processed data
        max_items: Maximum number of items to process (None for all items)
        language: Language code for extracting labels and descriptions
        num_processes: Number of processes to use (defaults to CPU count)
    """
    logger.info(f"Processing Wikidata dump: {dump_path}")
    
    if max_items:
        logger.info(f"Will extract up to {max_items} items from Wikidata dump")
    else:
        logger.info(f"Will extract all valid items from Wikidata dump")
    
    # Verify file exists and is a gzip file
    if not os.path.exists(dump_path):
        raise FileNotFoundError(f"Dump file not found: {dump_path}")
    
    # Check if it's a gzip file
    try:
        with gzip.open(dump_path, 'rb') as test:
            test.read(2)
    except gzip.BadGzipFile:
        raise ValueError(f"File is not a valid gzip file: {dump_path}")
    
    # Determine number of processes to use
    if num_processes is None:
        num_processes = multiprocessing.cpu_count()
    
    logger.info(f"Using {num_processes} processes for parallel processing")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    # Create a temporary directory for output chunks
    temp_dir = tempfile.mkdtemp(prefix="wikidata_processing_")
    logger.info(f"Using temporary directory: {temp_dir}")
    
    try:
        # Count lines and create chunks
        total_lines = count_lines_in_gzip(dump_path)
        chunks = split_file_into_chunks(total_lines, num_processes)
        
        # Calculate max items per chunk
        max_items_per_chunk = float('inf')
        if max_items is not None:
            max_items_per_chunk = max_items // num_processes
        
        # Prepare chunk parameters
        chunk_params = []
        temp_files = []
        
        for i, (start_line, end_line) in enumerate(chunks):
            temp_file = os.path.join(temp_dir, f"chunk_{i}.jsonl")
            temp_files.append(temp_file)
            
            # Add max_items_per_chunk to the parameters
            chunk_params.append((
                dump_path,
                temp_file,
                start_line,
                end_line - start_line,  # Calculate chunk_size as difference
                max_items_per_chunk,
                language
            ))
        
        # Process chunks in parallel
        start_time = time.time()
        
        with multiprocessing.Pool(processes=num_processes) as pool:
            # Use starmap to unpack the tuple arguments correctly
            results = pool.starmap(process_chunk, chunk_params)
            total_processed = sum(results)
        
        processing_time = time.time() - start_time
        logger.info(f"Parallel processing completed in {processing_time:.2f} seconds")
        logger.info(f"Total items processed: {total_processed}")
        
        # If max_items is set and we processed more, we need to truncate
        if max_items is not None and total_processed > max_items:
            logger.info(f"Limiting output to {max_items} items as requested")
            
            # Merge until we hit the limit
            remaining = max_items
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for temp_file in temp_files:
                    if remaining <= 0:
                        break
                        
                    if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                        with open(temp_file, 'r', encoding='utf-8') as infile:
                            for line in infile:
                                outfile.write(line)
                                remaining -= 1
                                if remaining <= 0:
                                    break
            
            logger.info(f"Completed processing. Saved {max_items} items to {output_path}")
        else:
            # Merge all output files
            logger.info("Merging output files...")
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for temp_file in temp_files:
                    if os.path.exists(temp_file) and os.path.getsize(temp_file) > 0:
                        with open(temp_file, 'r', encoding='utf-8') as infile:
                            shutil.copyfileobj(infile, outfile)
            
            logger.info(f"Completed processing. Saved {total_processed} items to {output_path}")
        
        return output_path
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)

def create_training_samples(input_path, output_path, min_length=50):
    """
    Create training samples from processed Wikidata.
    Filter out entries that are too short and prepare data in the right format.
    """
    logger.info(f"Creating training samples from {input_path}")
    
    count = 0
    with open(input_path, 'r', encoding='utf-8') as f_in:
        with open(output_path, 'w', encoding='utf-8') as f_out:
            for line in tqdm(f_in, desc="Creating training samples"):
                try:
                    item = json.loads(line)
                    
                    if 'text' in item and len(item['text']) >= min_length:
                        # Additional processing can be done here
                        f_out.write(json.dumps({'text': item['text']}) + '\n')
                        count += 1
                
                except Exception as e:
                    logger.error(f"Error processing line: {e}")
                    continue
    
    logger.info(f"Created {count} training samples in {output_path}")
    return output_path
    
def count_lines_in_gzip(file_path):
    """
    Count the number of lines in a gzipped file
    """
    logger.info(f"Counting lines in {file_path}...")
    count = 0
    
    try:
        with gzip.open(file_path, 'rt', encoding='utf-8') as f:
            for _ in f:
                count += 1
    except Exception as e:
        logger.error(f"Error counting lines: {e}")
        return 0
    
    logger.info(f"Total lines: {count}")
    return count

def split_file_into_chunks(total_lines, num_chunks):
    """
    Split a file with total_lines into num_chunks chunks
    Returns a list of (start_line, end_line) tuples
    """
    chunks = []
    
    # Calculate base lines per chunk
    lines_per_chunk = max(1, total_lines // num_chunks)
    
    # Create chunks
    for i in range(num_chunks - 1):
        start_line = i * lines_per_chunk
        end_line = (i + 1) * lines_per_chunk
        chunks.append((start_line, end_line))
    
    # Last chunk gets the remainder
    start_line = (num_chunks - 1) * lines_per_chunk
    chunks.append((start_line, total_lines))  # End at total_lines instead of infinity
    
    logger.info(f"Split into {len(chunks)} chunks with approx. {lines_per_chunk} lines each")
    return chunks

def main():
    parser = argparse.ArgumentParser(description='Advanced Wikidata Processor - Download, process, and format Wikidata dumps')
    
    # Main operation modes
    parser.add_argument('--download', action='store_true', help='Download Wikidata dump')
    parser.add_argument('--process', action='store_true', help='Process raw Wikidata dump')
    parser.add_argument('--list-dumps', action='store_true', help='List available Wikidata dump types')
    
    # Input and output options
    parser.add_argument('--dump-type', type=str, default='lexemes', 
                        help='Type of Wikidata dump to download (all, lexemes, truthy, properties)')
    parser.add_argument('--dump-url', type=str, help='URL to Wikidata dump (overrides dump-type)')
    parser.add_argument('--dump-path', type=str, help='Path to existing Wikidata dump')
    parser.add_argument('--output-dir', type=str, default='./wikidata_processed', help='Output directory')
    parser.add_argument('--output', type=str, help='Direct output file path (overrides output-dir)')
    
    # Processing options
    parser.add_argument('--max-items', type=int, default=None, 
                        help='Maximum items to process (default: all items)')
    parser.add_argument('--language', type=str, default='en', help='Preferred language code')
    parser.add_argument('--min-length', type=int, default=50, help='Minimum text length for training samples')
    
    # Parallel processing options
    parser.add_argument('--processes', type=int, default=None, 
                        help='Number of processes to use (default: number of CPU cores)')
    
    args = parser.parse_args()
    
    # List available dumps if requested
    if args.list_dumps:
        print("Available Wikidata dump types:")
        for dump_id, dump_info in WIKIDATA_DUMPS.items():
            print(f"  {dump_id}: {dump_info['name']}")
            print(f"      {dump_info['description']}")
            print(f"      URL: {dump_info['url']}")
            print()
        return
    
    # Create output directory
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    
    # Determine output paths
    if args.output:
        processed_path = args.output
        training_path = os.path.splitext(args.output)[0] + '_training.jsonl'
    else:
        processed_path = os.path.join(output_dir, 'wikidata_enhanced.jsonl')
        training_path = os.path.join(output_dir, 'wikidata_training.jsonl')
    
    # Download dump if requested
    dump_path = None
    if args.download:
        try:
            dump_path = download_wikidata_dump(
                output_dir=os.path.join(output_dir, 'dumps'),
                dump_type=args.dump_type,
                dump_url=args.dump_url
            )
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return
    else:
        dump_path = args.dump_path
    
    # Process dump if we have a valid path and processing is requested
    if dump_path and args.process:
        try:
            processed_path = process_wikidata_dump_parallel(
                dump_path=dump_path,
                output_path=processed_path,
                max_items=args.max_items,
                language=args.language,
                num_processes=args.processes
            )
        except Exception as e:
            logger.error(f"Error processing dump: {e}")
            return
    
    # Create training samples
    if args.process and os.path.exists(processed_path):
        create_training_samples(
            input_path=processed_path,
            output_path=training_path,
            min_length=args.min_length
        )
        
        logger.info(f"Processing complete. Enhanced data saved to {processed_path}")
        logger.info(f"Training data saved to {training_path}")

if __name__ == "__main__":
    main()
