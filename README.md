# User Manual for Automated Matching of Geographical Names and Shapefiles

## Purpose

The purpose of this solution is to match a list of place names in a dataset to the corresponding records and shapefiles in the official GADM database (Database of Global Administrative Areas). If all names are a direct match, then looking up every name is a simple SQL search away and this would be a simple task. However, it is often the case that the location names in a dataset are in a different language, contain spelling mistakes, or have a slightly different spelling than the official spelling in the GADM database. This makes the task of matching not so simple and straightforward.

![未命名绘图.drawio (2).png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/%25E6%259C%25AA%25E5%2591%25BD%25E5%2590%258D%25E7%25BB%2598%25E5%259B%25BE.drawio_(2).png)

The system consists of two parts. The first part matches the list of names to the GADM database, returning a dataset file (.csv/.excel) with all the matches, and a .txt file of all the matched indices for each item so that you could use it to match the shapefiles. The second part uses the matched indices tp returns the corresponding shapefiles from the GADM database, and turns the dataset file from the first part into a geopackage(.gpkg) file. 

In summary, the first part matches the list to the names and indices of the GADM database, while the second part matches to the shapefiles of the GADM database.

![未命名绘图.drawio (3).png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/%25E6%259C%25AA%25E5%2591%25BD%25E5%2590%258D%25E7%25BB%2598%25E5%259B%25BE.drawio_(3).png)

The first part is a web app developed using the streamlit framework and is hosted using streamlit’s free cloud services. The second part is a python jupyter notebook. Since not everyone has the environment set up to run python notebooks, I have been trying to compile a standalone windows .exe but I am having some troubles making it. 

### Why two separate components?

The shapefile matching process involves the full GADM database of the entire world which comes to 2.6GB. This is too big for the streamlit free cloud services to host and process, which is why the shapefile matching process has to be done locally. 

Separating the process into two parts also allows you to stop when you want. If you only want to match the names but not the shapefiles, you can stop after using the web app and completing the first part. 

## Usage

For name matching, you may access the web app here: 

[https://terbiume65-streamlit-automated-matching-prod-final-gu3bc3.streamlit.app/](https://terbiume65-streamlit-automated-matching-prod-final-gu3bc3.streamlit.app/)

For shapefile matching, you may download the files here:

[https://mega.nz/folder/PPoWFbpT#hOKpsm9cUSn4uNZnCNijCg](https://mega.nz/folder/PPoWFbpT#hOKpsm9cUSn4uNZnCNijCg)

### Using the web app for names matching

**Step 1: Access the website.** The app may be already up and running, or it may be in sleeping mode as shown below. The app would be in sleeping mode if the app have not been used for several days (the hosting service is free, so it puts unused apps to sleep to conserve resources). If it is in sleeping mode, click the blue button “Yes, get this app back up!”. This would tell the server to re-compile (”bake”) the app. The compiling process may take up to 20 minutes. After re-compiling, the app should be ready to use.

![Screenshot 2022-11-29 at 11.35.38 AM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-29_at_11.35.38_AM.png)

**Step 2: The app should look like this.** First, **choose the model**. If you want to match the names of countries to their ISO-3166 codes (i.e. Afghanistan → AFG, Algeria → DZA), click the “Country names matching” option. This would switch to a model where names are matched to a custom database of common alternate country names and their ISO-3166 codes, instead of the GADM database. If you want to match the names of places that are lower than the country scale (e.g. provinces, counties, etc.) to the GADM database, click “sub-country level geographical matching”

![Screenshot 2022-11-29 at 12.56.31 PM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-29_at_12.56.31_PM.png)

**Step 3: Upload your dataset.** You may drag and drop a file into the widget or click the “browse files” button to select a file. Files of .csv, .xls, .xlsx formats are accepted. Once the file is uploaded (the file name would appear), click the “submit” button below the widget to submit the file. If you selected the wrong file, click the “x” button on the right side of the file name to re-select. After you uploaded your dataset file and clicked the submit button, your dataset should be shown and a bunch of settings options should pop up below it.

![Screenshot 2022-11-29 at 2.54.08 PM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-29_at_2.54.08_PM.png)

**Step 4: Set up the matching process**

First, select the column in the dataset containing the place names that you want to be matched.

Second, set the similarity threshold for spelling correction. The model contains a spelling correction component such that similar alternative names for places/spelling mistakes could be matched. If you set this to a higher value, then there would be little spelling correction, since only corrections made with high similarity to the original word would go through. If you set this to a lower value, then there would be a lot of spelling correction, since even corrections made with low similarity to the original word would go through. Setting the value higher (less correction) may mean that there are fewer mistakes caused by excessive spelling correction, but items that are correctly matched because of spelling correction may also go away. 

Third, select the mode. You can choose unconstrained matching, which would return all relevant matches with the GADM database. On the other hand, if you know the specific country that the place name is in, you may choose constrained matching, and pass in an additional column of ISO-3166 code describing which country each place belongs to. Then, only the matches from the country you passed in would be returned and all the matches from the other countries would be ignored. 

Example:

Let’s say you are trying to match the following place names and passed this in as the column to be matched:

[Naples, Kingston, Cambridge]

If you set the mode to be “unconstrained”, then there may be multiple matches for each of these names:

[[Naples US, Naples Italy], [Kingston US, Kingston Jamaica], [Cambridge US, Cambridge UK]]

You may avoid such multiple matches if you choose “constrained matching” and pass in a column of ISO-3166 codes corresponding to the countries that each name is in:

[ITA, JAM, GBR]

Then, only the matches belonging to the countries passed would be returned:

[[Naples Italy], [Kingston Jamaica], [Cambridge UK]]

After everything is set, click the “match” button to start the matching process.

![Screenshot 2022-11-29 at 2.55.07 PM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-29_at_2.55.07_PM.png)

**Step 5: After clicking the “match” button, the matching process would start** and you would see a progress bar showing the progress of matching. The matching progress may take some time. If you have too many names to match, it is recommended that you split your dataset into several smaller batches so that matching would not take too long, as the server would may or may not stop the app if it is running for too long (20-30 minutes) (see troubleshooting which mentions this error).

![Screenshot 2022-11-29 at 3.50.27 PM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-29_at_3.50.27_PM.png)

**Step 6: When matching is complete, you would see the success message**, the sample output, and the download buttons to download the dataset with all the matches (as CSV or Excel file)m and also the download button to download a .txt file of all the matched indices. **You should download the CSV file and the matched indices .txt file if you want to move on to the second part of shapefile matching.**

![Screenshot 2022-11-29 at 3.52.30 PM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-29_at_3.52.30_PM.png)

Note: It is strongly recommended that you keep the tab open and keep an eye on the progress. Download the output as soon as possible when the matching is complete. Since streamlit cloud is a free hosting service, variables and cache are cleared regularly. Your output may disappear if left for too long. 

### Troubleshooting

**Problem: The app froze while matching and all the progress disappeared/ The app rebooted on its own while matching/ The app suddenly got back to the beginning**

Solution: How many items are you matching and how long have the app been running? It may be that you are trying too match too many items (>1500) or the app has been running for too long (>20 minutes). Try splitting your dataset into several batches and match it over several tries. For example, if you have a dataset of 2800 names, try splitting it into 4 smaller batches of 700 names and match it over 4 tries. 

**Problem: While waking up the app, it showed “oh no! something has gone wrong” or a similar error**

Solution: This is an unexplained server-side error during compiling. Streamlit is designed to only host lightweight and simple apps, so hosting this is already pushing it. Try refreshing and re-compiling a few more times. It is bound to succeed after several tries.

**Problem: Something weird happened/ Some error happened and refreshing the page doesn’t make the error go away/ I want to reboot the app but all the old output is still here**

Solution: Click the three-bar icon on the upper right hand corner. Click “rerun”. If that doesn’t work, click “clear cache” under developer options.

**Problem: Anything else not mentioned here.**

Solution: Since the app is already so big to be hosted on the free service, there are not a lot of error handling code so you may run into other errors not listed here. The first thing you could try is to make sure the column of names to be matched are completely clean (i.e. String only, no weird annotations/symbols/numbers, no empty rows, etc.). After that, rerun the app and clear cache as described in the solution above. If it still doesn’t work, contact me at terbiume65@gmail.com and I will attempt to debug it. 

### Using the local app for shapefile matching

After matching the names using the web app, you may go on to use the local app for shapefile matching to create a .gpkg file for GIS usage. You would need the CSV file and the matched indices .txt file from the web app when you completed name matching.

**Step 1: Download the app.ipynb file.** There is also a GADM world database .gpkg file. This is the exact mirror of the GADM world database. If you already have it on your local computer you don’t need to download it. If you don’t have it on your local computer, you should download it.

![Screenshot 2022-11-29 at 4.22.17 PM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-29_at_4.22.17_PM.png)

**Step 2: Run the jupyter notebook.** Enter the file path of the GADM database file, and the file paths of both the matched indices .txt file and the .csv file you got from the web app. Also enter the path you want for the output .gpkg file. Then, run all cells. 

Tip: if you are using Windows, shift + right mouse click, select “copy file path” quickly gives you the file path.

if you are using Mac, in Finder, choose View → Show path bar. Then, click on the file, it would show its path on the path bar. Control-click the file in the path bar, then choose “Copy “file” as Pathname”

Tip: if you do not have an environment set up to run jupyter notebooks, upload the .ipynb file and all the relevant files (GADM .gpkg, .csv, .txt) to Google Colab and run it

![Screenshot 2022-11-29 at 5.09.01 PM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-29_at_5.09.01_PM.png)

**Step 3: The output .gpkg file should now in the output file path that you specified.** You may use the .gpkg file in GIS applications.

![Screenshot 2022-11-30 at 2.44.53 PM.png](User%20Manual%20for%20Automated%20Matching%20of%20Geographical%20a164f8e617b24b099c8ee9f452b0fc32/Screenshot_2022-11-30_at_2.44.53_PM.png)