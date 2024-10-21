from magika import Magika
from magic import from_buffer
from mimetypes import guess_extension

def get_ext_and_mime(file, file_content: bytes) -> tuple[str, str]:
    # Get the user-provided MIME type
    u_file_mime = file.content_type
    print(f"[User] Identified file MIME: {u_file_mime}")

    # Use Magika to identify the file MIME type
    magika = Magika()
    mk_out = magika.identify_bytes(file_content).dl
    mk_file_mime = mk_out.mime_type if mk_out and hasattr(mk_out, 'mime_type') else None
    print(f"[Magika] Identified file MIME: {mk_file_mime}")

    # Use python-magic to identify the file MIME type
    mc_file_mime = from_buffer(file_content, mime=True)
    print(f"[Magic] Identified file MIME: {mc_file_mime}")
    
    # Collect MIME types and choose the most frequent one
    mimes = [u_file_mime, mk_file_mime, mc_file_mime]
    mimes = [mime for mime in mimes if mime]  # Remove None values
    m_type = max(set(mimes), key=mimes.count)  # Select the most frequent MIME

    # Get the file extension based on the final MIME type
    m_ext = guess_extension(m_type)
    
    # Handle edge cases where guess_extension returns None
    if not m_ext:
        m_ext = ".bin"  # Default to a generic binary extension if undetermined
    
    # Ensure the return values are strings
    return str(m_ext).lstrip("."), str(m_type)
