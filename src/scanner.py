import vt
import os
import asyncio

from dotenv import load_dotenv

load_dotenv()


VT_APIKEY = os.getenv("VIRUSTOTAL_APIKEY")
client = vt.Client(VT_APIKEY)

async def ScanFile(filepath):
    async with vt.Client(VT_APIKEY) as client:
        with open(filepath, "rb") as f:
            analysis = await client.scan_file_async(f, wait_for_completion=True)

        analysis = await client.get_object_async("/analyses/{}", analysis.id)

    return f'''
File : {filepath}
Summary :
{chr(10).join(f"{k}: {v}" for k, v in analysis.stats.items())}

Details :
{chr(10).join(f"{k}: {v}" for k, v in analysis.results.items())}
'''

async def ScanURL(url):
    async with vt.Client(VT_APIKEY) as client:
        analysis = await client.scan_url_async(url, wait_for_completion=True)
        analysis = await client.get_object_async("/analyses/{}", analysis.id)
        return f'''
Summary :
{chr(10).join(f"{k}: {v}" for k, v in analysis.stats.items())}

Details :
{chr(10).join(f"{k}: {v}" for k, v in analysis.results.items())}
'''


if __name__ == "__main__":
    
        # Build the absolute path to the PDF file in the parent directory
        filename = "01-Intro-to-SQL.pdf"
        filepath = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", filename))
        res = asyncio.run(ScanFile(filepath))
        # url = "http://ruehrdich.dnsdojo.org/.newsle/"
        # res = ScanURL(url)
        print(res)
 