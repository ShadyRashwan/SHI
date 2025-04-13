# Author: Shady Rashwan
# Streamlit GUI for Images to PDF Converter

import os
import streamlit as st
import tempfile
from PIL import Image
import shi as shi  # Import the main module

def set_page_config():
    """Configure the Streamlit page settings with Tailwind-inspired dark mode styling"""
    st.set_page_config(
        page_title="SHI - Images to PDF Converter",
        page_icon="📷",
        initial_sidebar_state="collapsed",
        menu_items={}
    )
    
    # Tailwind CSS inspired styling with dark mode
    st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Base dark mode theme */
    :root {
        color-scheme: dark;
    }
    
    .stApp {
        background-color: #111827; /* gray-900 */
        color: #e5e7eb; /* gray-200 */
    }
    
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #cadbfd !important; /* gray-100 */
    }
    
    /* Button styling - Pepsi Blue */
    .stButton button {
        background-color: #117FD7 !important; /* Pepsi blue */
        color: white !important;
        border-radius: 0.375rem !important;
        font-weight: 500 !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        transition: all 150ms ease-in-out !important;
    }
    
    .stButton button:hover {
        background-color: #006DC7 !important; /* Darker Pepsi blue */
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
    }
    
    /* Feature icon styling */
    .feature-icon {
        display: flex; /* Use flexbox for alignment */
        margin: 0 auto; /* Center the icon horizontally */
        align-items: center; /* Center content vertically */
        justify-content: center; /* Center content horizontally */
        background-color: transparent !important; /* Make the background transparent */
        color: #0078D7; /* Pepsi blue */
        height: 3rem;
        width: 3rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem; /* Adjust spacing between icon and text */
    }

    .feature-card h3 {
        text-align: center; /* Center-align the title text */
        margin: 0 0 0.5rem 0; /* Add spacing below the title */
    }

    .feature-card p {
        text-align: center; /* Center-align the description text */
        margin: 0; /* Remove default margins */
        color: #9ca3af; /* Gray text color */
        font-size: 0.875rem; /* Adjust font size */
    }
    
    /* Custom styling for Streamlit alerts - completely transparent background with bright text */
    div[data-baseweb="notification"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Force all notification containers to be transparent */
    div[data-baseweb="notification"] > div {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    
    /* Make the alert text bold and bigger */
    div[data-baseweb="notification"] div[role="alert"] {
        font-weight: 700 !important;
        font-size: 1.1rem !important;
        text-shadow: 0px 0px 3px rgba(0,0,0,0.5) !important;
    }
    
    /* Ultra bright colors for different alert types */
    div[data-kind="info"] div[role="alert"] {
        color: #38bdf8 !important; /* bright blue */
    }
    
    div[data-kind="success"] div[role="alert"] {
        color: #4ade80 !important; /* bright green */
    }
    
    div[data-kind="warning"] div[role="alert"] {
        color: #facc15 !important; /* bright yellow */
    }
    
    div[data-kind="error"] div[role="alert"] {
        color: #f87171 !important; /* bright red */
    }
    </style>
    """, unsafe_allow_html=True)

class OutputCapture:
    """Class to capture print outputs from the medical module"""
    def __init__(self):
        self.outputs = []
    
    def write(self, text):
        self.outputs.append(str(text))
    
    def flush(self):
        pass
    
    def get_output(self):
        return "\n".join(self.outputs)

def process_folder(folder_path, preserve_originals):
    """Process the folder with minimal display"""
    folder_path = normalize_path(folder_path)
    
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        st.error(f"Invalid path: '{folder_path}'")
        return
    
    # Simple status and progress display
    status = st.empty()
    progress = st.progress(0)
    
    # Set up output capture
    import sys
    original_stdout = sys.stdout
    capture = OutputCapture()
    sys.stdout = capture
    
    try:
        # Initial status
        status.info("Processing images...")
        
        # Simple progress tracking
        def check_progress():
            output = capture.get_output()
            if "Processing images" in output:
                progress.progress(0.2)
                status.info("Reading image files...")
            elif "Converting .heic" in output:
                progress.progress(0.4)
                status.info("Converting image formats...")
            elif "Creating PDF" in output:
                progress.progress(0.7)
                status.info("Creating PDF file...")
            elif "Finished creating:" in output:
                progress.progress(1.0)
                status.success("Conversion complete!")
        
        # Initial check
        check_progress()
        
        # Run the main function
        shi.create_pdf_from_images(folder_path, preserve_originals=preserve_originals)
        
        # Final progress update
        progress.progress(1.0)
        
        # Get output text to scan for results
        output = capture.get_output()
        
        # Extract basic results information
        pdf_count = 0
        pdf_files = []
        
        # Find main PDF file
        folder_name = os.path.basename(folder_path)
        expected_pdf = f"{folder_name}.pdf"
        pdf_path = os.path.join(folder_path, expected_pdf)
        
        if os.path.exists(pdf_path):
            pdf_count += 1
            pdf_files.append(pdf_path)
        
        # Find PDFs in subfolders (minimal check)
        for root, _, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.pdf') and os.path.join(root, file) not in pdf_files:
                    pdf_count += 1
        
        # Display celebratory results with Tailwind-style components
        if "Finished creating:" in output:
            # Update the status message to lime green
            deletion_text = " (original images deleted)" if not preserve_originals else ""
            status.success(f"Created {pdf_count} PDF file{'s' if pdf_count > 1 else ''} in {folder_path}{deletion_text}")
            
            # Create different HTML based on whether images were preserved or deleted
            if preserve_originals:
                success_html = f"""
                <div class="success-box" style="background-color: #1e1e1e !important; color: #84cc16 !important;">
                    <div style="display:flex; align-items:center; margin-bottom:1rem; gap:0.75rem;">
                        <div style="background-color:rgba(132, 204, 22, 0.2); height:2.5rem; width:2.5rem; border-radius:0.5rem; display:flex; align-items:center; justify-content:center;">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#84cc16" width="24" height="24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 style="margin:0; font-weight:600; color:#84cc16; font-size:1.125rem;">Success!</h3>
                    </div>
                    <div style="margin-left:0.5rem; display:flex; flex-direction:column; gap:0.75rem;">
                        <div style="display:flex; gap:0.75rem; align-items:center;">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#0078D7" width="20" height="20">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                            </svg>
                            <span style="color: #84cc16; font-weight: bold;">
                                {pdf_count} PDF{'s' if pdf_count > 1 else ''} saved in: 
                                <code style="background:#374151; padding:0.125rem 0.25rem; border-radius:0.25rem; font-size:0.875rem;">{folder_path}</code>
                            </span>
                        </div>
                    </div>
                </div>
                """
            else:
                success_html = f"""
                <div class="success-box" style="background-color: #1e1e1e !important; color: #84cc16 !important;">
                    <div style="display:flex; align-items:center; margin-bottom:1rem; gap:0.75rem;">
                        <div style="background-color:rgba(132, 204, 22, 0.2); height:2.5rem; width:2.5rem; border-radius:0.5rem; display:flex; align-items:center; justify-content:center;">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#84cc16" width="24" height="24">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                        </div>
                        <h3 style="margin:0; font-weight:600; color:#84cc16; font-size:1.125rem;">Success!</h3>
                    </div>
                    <div style="margin-left:0.5rem; display:flex; flex-direction:column; gap:0.75rem;">
                        <div style="display:flex; gap:0.75rem; align-items:center;">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#0078D7" width="20" height="20">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
                            </svg>
                            <span style="color: #84cc16; font-weight: bold;">
                                {pdf_count} PDF{'s' if pdf_count > 1 else ''} saved in: 
                                <code style="background:#374151; padding:0.125rem 0.25rem; border-radius:0.25rem; font-size:0.875rem;">{folder_path}</code>
                            </span>
                        </div>
                        <div style="display:flex; gap:0.75rem; align-items:center; margin-top:0.5rem;">
                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#f97316" width="20" height="20">
                                <path stroke-linecap="round" stroke-linejoin="round" d="M14.74 9l-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 01-2.244 2.077H8.084a2.25 2.25 0 01-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 00-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 013.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 00-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 00-7.5 0" />
                            </svg>
                            <span style="color: #f97316;">
                                Original images were deleted
                            </span>
                        </div>
                    </div>
                </div>
                """
            
            # Render the appropriate HTML
            st.markdown(success_html, unsafe_allow_html=True)
        else:
            status.warning("Process completed but no PDFs were created")
    
    except Exception as e:
        progress.progress(1.0)
        status.error("Conversion failed")
        st.error(str(e))
    
    finally:
        # Restore stdout
        sys.stdout = original_stdout

def display_welcome():
    """Display a decorated welcome header with separate feature cards"""
    # Title with icon
    st.markdown("""
    <h1 style="display:flex; align-items:center; gap:10px; margin-bottom:1.5rem;">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="32" height="32">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 14.25v-2.625a3.375 3.375 0 00-3.375-3.375h-1.5A1.125 1.125 0 0113.5 7.125v-1.5a3.375 3.375 0 00-3.375-3.375H8.25m2.25 0H5.625c-.621 0-1.125.504-1.125 1.125v17.25c0 .621.504 1.125 1.125 1.125h12.75c.621 0 1.125-.504 1.125-1.125V11.25a9 9 0 00-9-9z" />
        </svg>
        <span>SHI - Images to PDF Converter</span>
    </h1>
    """, unsafe_allow_html=True)
    
    # Create a styled "Why me?!" button that looks like a label
    col1, col2 = st.columns([4, 8])
    
    with col1:
        # First add the custom styling for the button
        st.markdown("""
        <style>
        /* Style the button to look like a label with dimmed blue background */
        div[data-testid="element-container"]:has(button:contains("🤔 Why me?! 🤷‍♂")) button {
            background-color: rgba(30, 67, 137, 0.15) !important;
            border: none !important;
            box-shadow: none !important;
            color: #4c7bd9 !important;
            font-weight: 600 !important;
            font-size: 1.3rem !important;
            padding: 8px 15px !important;
            border-radius: 8px !important;
            text-align: center !important;
            cursor: pointer !important;
            transition: all 0.2s !important;
            font-family: 'Source Sans Pro', sans-serif !important;
        }
        
        /* Hover effect */
        div[data-testid="element-container"]:has(button:contains("🤔 Why me?! 🤷‍♂")) button:hover {
            background-color: rgba(30, 67, 137, 0.25) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Then add the button that will trigger navigation to Why me page
        if st.button("🤔 Why me?! 🤷‍♂", key="why_me_button"):
            st.query_params["why_me"] = "true"
            st.rerun()
    
    # Create a 3-column layout for the feature cards
    cols = st.columns(3)
    
    # Feature 1: Format Support
    with cols[0]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="24" height="24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 15.75l5.159-5.159a2.25 2.25 0 013.182 0l5.159 5.159m-1.5-1.5l1.409-1.409a2.25 2.25 0 013.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 001.5-1.5V6a1.5 1.5 0 00-1.5-1.5H3.75A1.5 1.5 0 002.25 6v12a1.5 1.5 0 001.5 1.5zm10.5-11.25h.008v.008h-.008V8.25zm.375 0a.375.375 0 11-.75 0 .375.375 0 01.75 0z" />
                </svg>
            </div>
            <h3 style="font-size:1rem; font-weight:600; margin:0 0 0.5rem 0;">Format Support</h3>
            <p style="margin:0; color:#9ca3af; font-size:0.875rem;">JPG, PNG, GIF, BMP, TIFF and HEIC files supported</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 2: Recursive Processing
    with cols[1]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="24" height="24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 9.776c.112-.017.227-.026.344-.026h15.812c.117 0 .232.009.344.026m-16.5 0a2.25 2.25 0 00-1.883 2.542l.857 6a2.25 2.25 0 002.227 1.932H19.05a2.25 2.25 0 002.227-1.932l.857-6a2.25 2.25 0 00-1.883-2.542m-16.5 0V6A2.25 2.25 0 016 3.75h3.879a1.5 1.5 0 011.06.44l2.122 2.12a1.5 1.5 0 001.06.44H18A2.25 2.25 0 0120.25 9v.776" />
                </svg>
            </div>
            <h3 style="font-size:1rem; font-weight:600; margin:0 0 0.5rem 0;">Recursive Processing</h3>
            <p style="margin:0; color:#9ca3af; font-size:0.875rem;">Automatically processes images in all subfolders</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Feature 3: Quality Preservation
    with cols[2]:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" width="24" height="24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                </svg>
            </div>
            <h3 style="font-size:1rem; font-weight:600; margin:0 0 0.5rem 0;">Quality Preservation</h3>
            <p style="margin:0; color:#9ca3af; font-size:0.875rem;">Maintains image aspect ratios and quality in PDFs</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Warning message with Tailwind styling
    st.markdown("""
    <div class="warning-box">
        <div style="display:flex; align-items:flex-start; gap:0.75rem;margin: 0.5rem">
            <div style="margin-top:0.125rem;">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="#f59e0b" width="24" height="24">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m-9.303 3.376c-.866 1.5.217 3.374 1.948 3.374h14.71c1.73 0 2.813-1.874 1.948-3.374L13.949 3.378c-.866-1.5-3.032-1.5-3.898 0L2.697 16.126zM12 15.75h.007v.008H12v-.008z" />
                </svg>
            </div>
            <div>
                <h4 style="font-weight:600; color:#f59e0b; font-size:1rem;">Important</h4>
                <p style="margin:0,0,0,0.5; color:#fef3c7; font-size:0.875rem;">
                Please ensure you have backups of the folder before proceeding. Just in case 😈 
                </p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def normalize_path(path):
    """Normalize path across different operating systems"""
    if path:
        # Strip quotes that might have been copied/pasted
        path = path.strip('\'"')
        # Expand user directory (~ on Unix, %USERPROFILE% on Windows)
        path = os.path.expanduser(path)
        # Normalize path separators for the current OS
        path = os.path.normpath(path)
    return path

def on_path_change():
    """Callback function when the path input changes"""
    folder_path = st.session_state.folder_path_input
    
    # Don't revalidate if we haven't changed the path (prevents unnecessary work)
    if hasattr(st.session_state, 'last_validated_path') and st.session_state.last_validated_path == folder_path:
        return
    
    # Keep track of the last path we validated
    st.session_state.last_validated_path = folder_path
    
    # Mark that we need to force rerun of the app which helps with instant validation after paste
    st.session_state.need_rerun = True
    
    # Reset validation state
    st.session_state.valid_path = False
    st.session_state.path_info = ""
    st.session_state.current_valid_path = None
    st.session_state.current_image_count = 0
    
    if not folder_path:
        # Empty path - don't show any message
        return
    
    # Normalize path for cross-platform compatibility
    normalized_path = normalize_path(folder_path)
    
    # First just check if path exists and is a directory - quick check
    if not os.path.exists(normalized_path) or not os.path.isdir(normalized_path):
        st.session_state.path_info = "❌ Invalid folder path"
        return
    
    # If we get here, path exists, now count images
    try:
        # Start a count
        image_count = 0
        
        # Count images in folder (use a generator to be more efficient)
        for root, _, files in os.walk(normalized_path):
            for file in files:
                if any(file.lower().endswith(ext) for ext in shi.IMAGE_EXTENSIONS):
                    image_count += 1
                    # For efficiency, if we found some images we could stop counting
                    # after a reasonable number, but we'll count all for accuracy
        
        # Valid path with images
        if image_count > 0:
            path_info = f"✅ Found {image_count} image{'s' if image_count > 1 else ''}"
            
            # Store valid path information
            st.session_state.valid_path = True
            st.session_state.current_valid_path = normalized_path
            st.session_state.current_image_count = image_count
            st.session_state.path_info = path_info
        else:
            # Valid path but no images
            st.session_state.path_info = "⚠️ No images found in this folder"
    except Exception as e:
        # Handle any unexpected errors during validation
        st.session_state.path_info = f"❌ Error validating path: {str(e)}"

class PathWatcher:
    """Class to watch path input and trigger validation without Enter key."""
    def __init__(self):
        # Initialize or get current path value
        if 'current_path' not in st.session_state:
            st.session_state.current_path = ""
        
        # Setup on_change callback to detect input changes
        if 'folder_path_input' not in st.session_state:
            st.session_state.folder_path_input = ""
        
        # Add key checking for auto-validation 
        if 'last_input_value' not in st.session_state:
            st.session_state.last_input_value = ""
    
    def on_input_change(self):
        """Called when user modifies input"""
        # Always validate when input changes
        on_path_change()
        
        # Re-enable convert button if user is entering a new path
        if st.session_state.folder_path_input.strip():
            st.session_state.convert_disabled = False
    
    def render_input(self):
        """Render the text input with real-time validation"""
        # Create persistent container to avoid re-renders
        input_container = st.container()
        
        with input_container:
            # Reset the input field if processing is complete and user hasn't entered something new
            if st.session_state.processing_complete and not st.session_state.last_input_value:
                st.session_state.folder_path_input = ""
                st.session_state.processing_complete = False
            
            # Create text input with on_change callback
            folder_path = st.text_input(
                "Enter folder path:",
                placeholder="/path/to/folder/with/images",
                key="folder_path_input",
                label_visibility="collapsed",
                on_change=self.on_input_change  # Trigger validation on change
            )
            
            # Auto-validate on paste without requiring Enter
            if folder_path != st.session_state.last_input_value:
                st.session_state.last_input_value = folder_path
                # Force validation immediately without waiting for on_change
                on_path_change()
                # Set flag to force rerun (this is critical for validation to show immediately)
                st.session_state.need_rerun = True
        
        # Check if we have a valid path in session state
        valid_path = st.session_state.get("valid_path", False)
        normalized_path = st.session_state.get("current_valid_path", None) if valid_path else None
        
        return normalized_path

def folder_browser():
    """Create a simple folder browser with auto-validation on paste"""
    # Use the path watcher class to manage input and validation
    path_watcher = PathWatcher()
    
    # Render the input and get the result
    return path_watcher.render_input()

def show_platform_specific_help():
    """Show help specific to the user's operating system"""
    import platform
    system = platform.system()
    
    st.subheader("Tips for Your Operating System")
    
    if system == "Windows":
        st.info("""
        **Windows Path Tips:**
        - Use either forward slashes or double backslashes: `C:/Users/Username/Pictures` or `C:\\Users\\Username\\Pictures`
        - You can copy-paste from Windows Explorer's address bar
        - Example: `C:/Users/Username/Downloads/images`
        """)
    
    elif system == "Darwin":  # macOS
        st.info("""
        **macOS Path Tips:**
        - Use forward slashes: `/Users/username/Pictures`
        - You can drag a folder from Finder to Terminal to get the path, then copy it here
        - The tilde (~) is automatically expanded to your home directory
        - Example: `~/Downloads/images` or `/Users/username/Downloads/images`
        """)
    
    elif system == "Linux":
        st.info("""
        **Linux Path Tips:**
        - Use forward slashes: `/home/username/Pictures`
        - You can type `pwd` in terminal when in your folder to get the path
        - The tilde (~) is automatically expanded to your home directory
        - Example: `~/Downloads/images` or `/home/username/Downloads/images`
        """)
    
    else:
        st.info("""
        **Path Tips:**
        - Use the appropriate path format for your operating system
        - Make sure the folder exists and is accessible
        - Check for typos in the path
        """)

def display_why_me():
    """Display the Why Me page with comic style formatting"""
    # Read the markdown file
    try:
        # Use UTF-8 encoding to handle special characters
        with open("app/why_me.md", "r", encoding="utf-8") as f:
            why_me_content = f.read()
        
        # Display the back button separately using Streamlit's native button
        st.markdown(why_me_content, unsafe_allow_html=True)
        
        # Center align the button with columns
        col1, col2, col3 = st.columns([3, 2, 3])
        with col2:
            # Custom CSS for more elegant button using standard app styling
            st.markdown("""
            <style>
            /* Style the back button to match app standards */
            div[data-testid="element-container"]:has(button:contains("👋 Back to SHI")) button {
                background-color: #117FD7 !important; /* Pepsi blue to match app theme */
                color: white !important;
                border-radius: 0.375rem !important;
                font-weight: 500 !important;
                border: none !important;
                padding: 0.5rem 1rem !important;
                transition: all 150ms ease-in-out !important;
            }
            
            div[data-testid="element-container"]:has(button:contains("👋 Back to SHI")) button:hover {
                background-color: #006DC7 !important; /* Darker Pepsi blue */
                box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Add a Streamlit button with emoji
            if st.button("👋 Back to SHI", type="primary", use_container_width=True):
                # Clear query parameters
                st.query_params.clear()
                # Force rerun to reload the main page
                st.rerun()
    
    except Exception as e:
        # Show the specific error for debugging
        st.error(f"Error loading Why Me content: {str(e)}")
        
        # Try to load embedded content as fallback
        embedded_content = """
        # 🤔 Why me?! 🤷‍♂️

        ## The things YOU need to do first:

        1. You still have to take photos, I can't do it for you! 📸
        2. I'm not a taxi. Move images from phone to computer! 🚕
        3. Make folders with relevant names to contain your images 📁
        4. I'm off today, can you do it on your own? 😴
        5. I need that parent folder path. Let me take it from here! 🦸‍♂️

        Man 😅 I'm here to batch convert your images to PDF! 🎉
        """
        
        st.markdown(embedded_content)
        
        # Add a back button
        if st.button("Back to Converter"):
            # Clear query parameters
            st.query_params.clear()
            st.rerun()

def main():
    # Initialize processing_complete flag if not exist
    if "processing_complete" not in st.session_state:
        st.session_state.processing_complete = False
    
    # Initialize convert_disabled flag if not exist
    if "convert_disabled" not in st.session_state:
        st.session_state.convert_disabled = False
        
    # Check if we need to force a rerun from a paste event
    if st.session_state.get("need_rerun", False):
        st.session_state.need_rerun = False
        st.rerun()
    
    # Set page configuration and styling
    set_page_config()
    
    # Check for why_me parameter in query string using the non-experimental API
    query_params = st.query_params
    if "why_me" in query_params and query_params["why_me"] == "true":
        display_why_me()
        return
    
    # Show application header
    display_welcome()
    
    # Removed sidebar content
    
    # Add a label above the input
    st.write("""
             Paste the path to the folder containing your images 🥸
             press 'Enter'
             """)
    # Folder input that validates path
    folder_path = folder_browser()
    
    # Display image count below the text box if path is entered
    if "path_info" in st.session_state and st.session_state.path_info:
        # Add spacing and styling to the path info message
        st.markdown(f"<div class='path-info'>{st.session_state.path_info}</div>", unsafe_allow_html=True)
    
    # Delete checkbox and Convert button (only if path is valid)
    if "valid_path" in st.session_state and st.session_state.valid_path:
        # Create columns for checkbox and button
        col1, col2, col3 = st.columns([3, 1, 2])
        
        # Checkbox for deleting files in first column
        with col1:
            # Create a container for better layout control
            delete_container = st.container()
            
            # Add a flex container styling for alignment
            st.markdown("""
            <style>
            /* Create a flex container for the delete section */
            .delete-container {
                display: flex;
                align-items: center;
                gap: 8px;
                background-color: transparent !important;
            }
            
            /* Style the label */
            .delete-label {
                color: #ef4444;
                font-weight: bold;
                margin: 0;
                background-color: transparent !important;
            }
            
            /* Fix checkbox styling */
            .stCheckbox {
                background-color: transparent !important;
                margin-top: 0 !important;
                margin-bottom: 0 !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            # Use a single container with custom styling
            with delete_container:
                # First add the checkbox
                delete_originals = st.checkbox(
                    "Delete images (Keep PDFs only)",
                    value=False,
                    key="delete_images_checkbox",
                    help="Check this box if you want to permanently delete the images after creating the PDF"
                )
                
                # Override the styling with more targeted CSS
                st.markdown("""
                <style>
                /* Target the specific checkbox label */
                [data-testid="stCheckbox"] label p,
                .stCheckbox label p,
                div[key="delete_images_checkbox"] p,
                div[key="delete_images_checkbox"] label span,
                div[key="delete_images_checkbox"] label {
                    color: #ffc264 !important;
                    background-color: transparent !important;
              
                }
                
                # /* Remove any spacing between checkbox and label */
                # .stCheckbox > div > div {
                #     display: flex !important;
                #     align-items: center !important;
                #     gap: 4px !important;
                #     background-color: transparent !important;
                # }
                </style>
                """, unsafe_allow_html=True)
        
        # Convert button in second column
        with col2:
            convert_clicked = st.button(
                "Convert", 
                type="primary",
                key="convert_path_btn",
                use_container_width=True,
                disabled=st.session_state.convert_disabled
            )
            
        # Empty third column to create space on the right
        with col3:
            pass
            
        # If convert clicked, process the folder
        if convert_clicked:
            # Disable the button to prevent multiple clicks
            st.session_state.convert_disabled = True
            # Set processing complete flag to clear input after processing
            st.session_state.processing_complete = True
            # Clear the last input value to reset state
            st.session_state.last_input_value = ""
            
            st.write("---")
            # Process the folder (preserve_originals is the opposite of delete_originals)
            process_folder(folder_path, preserve_originals=not delete_originals)
    
    # Footer with "Made with love" text in Tailwind style
    st.write("")
    st.markdown("""
    <div style="text-align:center; padding:1rem; margin-top:2rem; border-top:1px solid #374151;">
        <div style="display:flex; align-items:center; justify-content:center; gap:0.5rem; color:#9ca3af; font-size:0.875rem;">
            <span>Made with</span> 
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="#ef4444" width="16" height="16">
                <path d="M11.645 20.91l-.007-.003-.022-.012a15.247 15.247 0 01-.383-.218 25.18 25.18 0 01-4.244-3.17C4.688 15.36 2.25 12.174 2.25 8.25 2.25 5.322 4.714 3 7.688 3A5.5 5.5 0 0112 5.052 5.5 5.5 0 0116.313 3c2.973 0 5.437 2.322 5.437 5.25 0 3.925-2.438 7.111-4.739 9.256a25.175 25.175 0 01-4.244 3.17 15.247 15.247 0 01-.383.219l-.022.012-.007.004-.003.001a.752.752 0 01-.704 0l-.003-.001z" />
            </svg>
            <span>by Shady Rashwan</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()