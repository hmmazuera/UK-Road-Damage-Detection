import streamlit as st
from PIL import Image
from ultralytics import YOLO

@st.cache_resource
def load_model():
    return YOLO('models/best.pt')

model = load_model()

st.title('AI Road Infrastructure Inspector')

uploaded_file = st.file_uploader('Upload a road image',
                                 type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert('RGB')
    st.image(image, caption='Uploaded Image')

    if st.button('Detect damage'):
        result = model.predict(image, conf=0.25, device='cpu')[0]

        st.image(result.plot(), channels='BGR', caption='Detection result')

        if len(result.boxes) == 0:
            st.write('No damage detected.')
        else:
            recommendations = {
                "Pothole": "Inspect the pothole and assess patching requirements.",
                "Alligator Crack": "Inspect pavement deterioration and assess repair requirements.",
                "Lateral Crack": "Inspect the crack and assess sealing requirements.",
                "Longitudinal Crack": "Inspect the crack and assess sealing requirements."
            }

            for box in result.boxes:
                name = result.names[int(box.cls.item())]
                confidence = box.conf.item()

                st.write(f'{name}: {confidence:.2f}')
                st.write(recommendations[name])