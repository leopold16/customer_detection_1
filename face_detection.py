import os
from deepface import DeepFace
from fer import FER
import logging

def detect_face(image_path):
    try:
        local_db_path = "./local_db"  # Path to your local image database

        model_name = 'ArcFace'
        distance_metric = 'cosine'
        threshold = 0.6

        # Perform face recognition
        results = DeepFace.find(img_path=image_path, db_path=local_db_path, model_name=model_name, distance_metric=distance_metric)

        # Perform emotion detection
        detector = FER(mtcnn=True)
        emotion_results = detector.detect_emotions(image_path)
        if emotion_results:
            emotion = emotion_results[0]['emotions']
            dominant_emotion = max(emotion, key=emotion.get)
        else:
            dominant_emotion = "No emotion detected"

        if isinstance(results, list):
            match_found = False
            for df in results:
                df['folder_name'] = df['identity'].apply(lambda x: x.split('/')[-2])
                folder_names = df['folder_name'].unique()
                if len(folder_names) > 0:
                    match_found = True
                    return folder_names[0], dominant_emotion  # Return the first match and emotion
            if not match_found:
                return "no matches found", dominant_emotion
        else:
            results['folder_name'] = results['identity'].apply(lambda x: x.split('/')[-2])
            folder_names = results['folder_name'].unique()
            if len(folder_names) > 0:
                return folder_names[0], dominant_emotion  # Return the first match and emotion
            else:
                return "no matches found", dominant_emotion
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        return "error", "No emotion detected"

    return "no matches found", "No emotion detected"
