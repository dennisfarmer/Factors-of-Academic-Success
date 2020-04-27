# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 10:38:39 2020

@author: Dennis
"""
import pandas

def split_dataframe(df:"pandas.DataFrame, pandas.Series", sections:"int"=5, drop_index:"bool"=True, output:"str"="dataframe")-> "None or pandas.DataFrame":
    """Display a single Dataframe across multiple columns in a Jupiter Notebook.
    
    Parameters
    ----------
        df : pandas.Dataframe, pandas.Series
        
        sections : int, default 5
            Number of columns to display.
            
        drop_index : bool, default True
            Determines whether to reset the original index. By default, the index is reset to integer values.
            
        output : {'dataframe', 'html'}, default 'dataframe'
            The kind of object to return
            - 'dataframe' returns a pandas.DataFrame object
            - 'html' displays an HTML table inline, with no return value
        
    Returns
    -------
        None or pandas.DataFrame
    
    """
    import numpy as np
    from IPython.display import display_html
    
    if sections <= 0:
        raise ValueError('number sections must be larger than 0.')
    
    ### Find out how to keep column names when dropindex=True
    ### if series, dont allow drop index?
    
    ### allow passing in of desired column names as an array of strings (will result
    ### in dup col names but it won't matter if its only being displayed and not used in calculations)

    if isinstance(df, pandas.Series):
        df = df.to_frame()
        
    if drop_index:
        df.reset_index(drop = True, inplace=True)
    else:
        df.reset_index(level=0, inplace=True)

    df_split = np.array_split(df, sections)
    num_rows = [column.shape[0] for column in df_split]
    
    if output == "dataframe":
        
        alldata = [column.values.tolist() for column in df_split]
        
        # Add empty rows to each DataFrame until all DataFrames have the same number of rows
        for i in range(len(alldata)):
            while len(alldata[i]) < max(num_rows):
                alldata[i].append([""]*df.shape[1])

        # Create rows of values across all of the DataFrames in alldata
        # When each entire row is created, add it to the output DataFrame
        dataframe = [] # <-- Output DataFrame
        for row_index in range(max(num_rows)):
            across_row = []
            for dataf in alldata:
                across_row.extend(dataf[row_index])
            dataframe.extend([across_row])
            
        return pandas.DataFrame(data=dataframe)
    
    if output == "html":
        strHtml = ''
        for x in split_dataframe:
            strHtml += x.to_html()
        display_html(strHtml.replace('table','table style="display:inline"'), raw=True)
        
        

def display_side_by_side(*args:"pandas.DataFrame, pandas.Series", drop_index:"bool"=False)-> "None":
    """Display multiple DataFrames side-by-side in a Jupiter Notebook.
    
    Parameters
    ----------
    *args : pandas.DataFrame or pandas.Series
        
    drop_index : bool, default False
        Determines whether to reset the index of each DataFrame. By default, all indexes are kept.
    
    Returns
    -------
    None

    """
    from IPython.display import display_html
    
    strHtml = ''
    for df in args:
        
        if isinstance(df, pandas.Series):
            df = df.to_frame()
        if drop_index:
            df.reset_index(drop=True, inplace=True)
            
        strHtml += df.to_html()
    display_html(strHtml.replace('table','table style="display:inline"'), raw = True)
    


if __name__ == "__main__":
    print("Charlie don’t surf!",
          "https://www.youtube.com/watch?v=yVcG0cTtSVo",
          "https://open.spotify.com/album/2UxN3UKyS3Z5r0Sra8A5RF?highlight=spotify:track:5T4j3Uv33fQO7tsR2lMl4y",
          sep="\n\n")
    
    
    
# add .todataframe (with concat or something)
