import pathlib
import shutil
import os 
import xml.etree.ElementTree as ET

class ExcelHandler:
    
    class XMLPicture:
        def __init__(self, row, name) -> None:
            self.row = row
            self.name = name
        
    def __init__(self):
        self.dir_extract = './'
        self.ns = {'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing'}
    
    def get_lst_images(self, sheetId :str) -> list:
        drawing = ET.parse(f"{self.dir_extract}/temp/xl/drawings/drawing{sheetId}.xml")
        ele = drawing.findall("xdr:oneCellAnchor", self.ns)
        res = []
        for idx, anchor in enumerate(ele, start=1):
            from_element = anchor.find('xdr:from', self.ns)
            col = from_element.find('xdr:col', self.ns).text
            row = from_element.find('xdr:row', self.ns).text
            pic_name = anchor.find('xdr:pic/xdr:nvPicPr/xdr:cNvPr', self.ns).attrib['name']
            res.append(self.XMLPicture(row, pic_name))
            
        return sorted(res, key=lambda x: x.row, reverse=False)

    def get_index_page(self):
        ns = {'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main', 'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
        workbook = ET.parse(f"{self.dir_extract}/temp/xl/workbook.xml")
        ele = workbook.find("sheets", namespaces=ns)
        for e in ele.iter():
            if e.get("name").startswith("case"):
                return e.get("sheetId"), ele[-1].get("sheetId")
        return None, None
    
    def extract_images_from_excel(self, path, dir_extract="./"):
        """extracts images from excel and names then with enumerated filename
        
        Args:
            path: pathlib.Path, excel filepath
            dir_extract: pathlib.Path, default=None, defaults to same dir as excel file
        
        Returns:
            new_paths: list[pathlib.Path], list of paths to the extracted images
        """
        if type(path) is str:
            path = pathlib.Path(path)
        if path.suffix != '.xlsx':
            raise ValueError('path must be an xlsx file')
        if os.path.exists(f"{dir_extract}/temp"):
            shutil.rmtree(f"{dir_extract}/temp")
        name = path.name.replace(''.join(path.suffixes), '').replace(' ', '') # name of excel file without suffixes
        temp_file = pathlib.Path(dir_extract) / 'temp.xlsx' # temp xlsx
        temp_zip = temp_file.with_suffix('.zip') # temp zip
        shutil.copyfile(path, temp_file)
        temp_file.rename(str(temp_zip))
        extract_dir =  temp_file.parent / 'temp'
        extract_dir.mkdir(exist_ok=True)
        shutil.unpack_archive(temp_zip, extract_dir) # unzip xlsx zip file
        os.remove(temp_zip)
        
EH = ExcelHandler()
print(EH.get_index_page()) # ('1', '2')