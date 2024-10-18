from magika import Magika
from magic import from_buffer
from mimetypes import guess_extension

# This one is a bit overkill, but its also for demonstration/learning purposes
def get_ext_and_mime(file, file_content: bytes) -> tuple[str, str]:

    u_file_mime = file.content_type
    print(f"[User] Identified file MIME: {u_file_mime}")

    magika = Magika()
    mk_out = magika.identify_bytes(file_content).dl
    mk_file_mime = mk_out.mime_type
    print(f"[Magika] Identified file MIME: {mk_file_mime}")

    mc_file_mime = from_buffer(file_content, mime=True)
    print(f"[Magic] Identified file MIME: {mc_file_mime}")
    
    mimes = [u_file_mime, mk_file_mime, mc_file_mime]
    m_type = max(set(mimes), key=mimes.count)
    # print(f"[Vote] Identified file MIME: {m_type}")
    m_ext = guess_extension(m_type).lstrip(".")
    return m_ext, m_type