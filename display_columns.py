# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 10:38:39 2020

@author: Dennis
"""
import pandas

def divide_dataframe(df:"pandas.DataFrame, pandas.Series", display_columns:"int", drop_index:"bool"=True)-> "None":
    """Display a single Dataframe across multiple columns in a Jupiter Notebook.
    
    Parameters
    ----------
        df : pandas.Dataframe, pandas.Series
        
        display_columns : int
            Number of columns to display.
            
        drop_index : bool, default True
            Determines whether to reset the original index. By default, the index is reset to integer values.
        
    Returns
    -------
        None
    
    """
    import numpy as np
    from IPython.display import display_html
    
    if display_columns < 2:
        raise IndexError('Number of desired columns must exceed 1')
    
    #if display_columns == df.shape[0]//display_columns:
        #raise ValueError('Number of rows cannot equal display_columns**2 for mathematical wizardry reasons') <-- not actually because of squared number
    
        # len(r)-1 ends up not being equal to display_columns
        # ^ Results in inaccurate number of rows shown
        
        # for df.shape[0] == 49:
        # when display_columns = 7...   actual_columns_displayed = 6
        # when display_columns = 10...  actual_columns_displayed = 11
        # etc...
        # (eventually I'll come back to this to figure out why)
        # (the likely solution is just to stick '+1' and '-1' everywhere lol)
    
    # Create range of indexes to divide DataFrame into multiple columns
    r = np.arange(0,df.shape[0],df.shape[0]//display_columns)
    # Add remainder rows to last column
    r[-1] = df.shape[0] - 1
    
    if drop_index:
        df.reset_index(drop=True, inplace=True)
    
    if isinstance(df, pandas.Series):
        df = df.to_frame()
    
    # Create list of DataFrames, where each DataFrame is a slice of the original DataFrame
    split_dataframe = [df[r[i]:r[i+1]+1] if i == display_columns-1 else df[r[i]:r[i+1]] for i in range(len(r)-1)]
    
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
