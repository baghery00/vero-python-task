import argparse, requests
import pandas as pd
from datetime import datetime
import logging as logger
logger.getLogger().setLevel(logger.INFO)

# jinja2 and openpyxl and matplotlib are this script deependencies
def main():

    def style(s, props='', color_indx=0, hu_indx=0, lbl=False, clr=False):
        stl = list(map(lambda x:'' , s.values))
        color = s.values[color_indx]
        if lbl and isinstance(color,str):
            color = color.split(' ')[0]  # in the case that we have two color code
            stl = list(map(lambda x: f'color:{color}' , stl))

        #if the -c flag is True, color each row 
        d = s.values[hu_indx]
        if clr and isinstance(d,str):
            now = datetime.now().date()
            hu = datetime.strptime(d, '%Y-%m-%d').date()
            dif = (hu - now).days
            clr = ""
            if dif<90: clr="#007500"
            elif dif<365: clr="#FFA500"
            else: clr="#b30000"
            stl = list(map(lambda x: f'{x}; background-color:{clr}', stl))
        return stl

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-c', '--colored', default=True)
    parser.add_argument('-k', '--keys')
    parser.add_argument('-f', '--file', default="vehicles.csv")
    args = parser.parse_args()
    colored = str(args.colored).lower() == 'true'
    keys = args.keys.split(',')
    try:
        file = open(args.file, 'rb')
        res = requests.put("http://127.0.0.1:8000/api/vehicles/", files={'file':file})
        if res.status_code != 200:
            raise Exception(f"please check the http connection")
        df = pd.DataFrame(res.json()).sort_values(by=["gruppe"]) #Rows are sorted by response field gruppe

        #Columns always contain rnr field
        if 'rnr' not in df.columns:
            raise KeyError("Data doesn't contain <rnr> field")

        #Only keys that match the input arguments are considered as additional columns (i.e. when the script is invoked with kurzname and info, print two extra columns)
        extra_keys = list(map(lambda x: x+"_extra" ,keys))
        extra_cols = df[keys].rename( columns = dict(zip(keys, extra_keys)))
        df = pd.concat([df,extra_cols], axis=1)

        #styling
        df = df.style.apply(style, 
                            color_indx = df.columns.get_loc('colorCode') , 
                            hu_indx= df.columns.get_loc('hu'), 
                            lbl = 'labelIds' in keys, #If labelIds are given and at least one colorCode could be resolved, use the first colorCode to tint the 
                            clr = colored, #if the -c flag is True, color each row
                            axis=1)
        file_name = f"vehicles_{datetime.now().date().isoformat()}.xlsx"
        df.to_excel(file_name)
        logger.info(f"Process finished succesfuly and you can find the result in {file_name}")
    except IOError as ioerr:
        logger.error(f"There is an error: please check the .csv file")
    except  Exception as err:
        logger.error(f"There is an error: {str(err)}")
    finally:
        if 'file' in locals():
            file.close()


if __name__ == "__main__":
   main()