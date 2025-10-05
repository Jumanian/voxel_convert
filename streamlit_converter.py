"""
Roblox Voxel Map Converter - Streamlit Web App
"""

import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="Voxel Map Converter", page_icon="🎮")

st.title("🎮 Voxel Map Converter")
st.write("Convert country images to Roblox voxel maps")

# File upload
uploaded_file = st.file_uploader(
    "Upload your black & white country image",
    type=["png", "jpg", "jpeg", "bmp"]
)

# Map size slider
map_size = st.slider("Map Size", min_value=20, max_value=300, value=100)

st.info("ℹ️ Black pixels = Land | White pixels = Water")

if uploaded_file is not None:
    # Display uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", width=300)
    
    # Convert button
    if st.button("Convert to Roblox Format", type="primary"):
        with st.spinner("Converting..."):
            # Process image
            img = image.convert('L')
            
            # Resize if needed
            if img.width > map_size or img.height > map_size:
                ratio = min(map_size / img.width, map_size / img.height)
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            pixels = img.load()
            width, height = img.size
            
            # Generate data in Roblox format
            output = "-- Auto-generated voxel map data\n"
            output += f"-- Dimensions: {width}x{height}\n\n"
            output += "return {\n"
            
            voxel_count = 0
            for y in range(height):
                output += "\t{"
                row = []
                for x in range(width):
                    value = "1" if pixels[x, y] < 128 else "0"
                    row.append(value)
                    if value == "1":
                        voxel_count += 1
                output += ",".join(row)
                output += "},\n"
            
            output += "}\n"
            
            # Success message
            st.success(f"✅ Conversion complete! Map size: {width}x{height} | Voxels: {voxel_count:,}")
            
            # Download button
            st.download_button(
                label="📥 Download mapData.txt",
                data=output,
                file_name="mapData.txt",
                mime="text/plain"
            )
            
            # Show preview of data
            with st.expander("Preview Generated Data"):
                st.code(output[:500] + "..." if len(output) > 500 else output, language="lua")
            
            # Instructions
            st.markdown("---")
            st.markdown("### 📋 Next Steps:")
            st.markdown("""
            1. Download the `mapData.txt` file above
            2. Open Roblox Studio
            3. Create a **ModuleScript** in ReplicatedStorage
            4. Name it **"MapData"**
            5. Copy the contents of `mapData.txt` into it
            6. Use the Roblox generator script to build your map!
            """)
else:
    st.info("👆 Upload an image to get started!")
    
# Footer
st.markdown("---")
st.caption("Made for Roblox voxel map generation")
