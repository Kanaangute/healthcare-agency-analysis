import pandas as pd
df = pd.read_csv('cms_data.csv') # read the csv file and convert it into a pandas dataframe

print(df.head()) #look at the first few rows, basically a preview

print(f"Total rows: {len(df)}") #get the length of rows
print(f"Total columns: {len(df.columns)}") #get the length of columns

print ("\nstar rating distribution") 
print (df['Quality of patient care star rating'].value_counts()) #selects patient care star rating column, and counts hoow many times each unique value appears

print (f"\nAverage star rating")
cleaned_patient_star_ratings = pd.to_numeric(df['Quality of patient care star rating'], errors='coerce') #converts all non-numeric values to NaN
print (round(cleaned_patient_star_ratings.mean(), 2)) #calculates the average or mean of the patient star rating

print(f"Agencies with ratings: {cleaned_patient_star_ratings.notna().sum()}") #bool - agencies with ratings that are valid
print(f"Agencies missing ratings: {cleaned_patient_star_ratings.isna().sum()}") #bool - agencies with ratings that are NaN

print(f"\nAverage star rating by distribution")
df['cleaned_patient_star_ratings'] = pd.to_numeric(df['Quality of patient care star rating'], errors='coerce') #takes the cleaned star rating data and created a new column of them
df_filtered = df[df['Type of Ownership'] != '-'] #filters out the null values in the ownership type column
avg_by_ownership = df_filtered.groupby('Type of Ownership')['cleaned_patient_star_ratings'].mean() #groups data by two categories and calculates their averages
print(avg_by_ownership.round(2)) # two decimals

print(f"\nHow many agencies had invalid values for ownership type:")
print(len(df) - len(df_filtered)) # how many null values that were filtered out

print(f"\nTtop 10 states by average star rating")
df_with_ratings = df[df['cleaned_patient_star_ratings'].notna()] #removes rows that dont have a rating
avg_by_state = df_with_ratings.groupby('State')['cleaned_patient_star_ratings'].mean() #group by state and calculate the average

top_states = avg_by_state.sort_values(ascending = False).head(10) #sorts the states in descending order and prints top 10
print(top_states.round(2)) 

print(f"\nBottom 10 states by average star rating")
bottom_states = avg_by_state.sort_values(ascending = False).tail(10) #sorts the states in ascending order and prints bottom 10
print(bottom_states.round(2))

print(f"\nMassachusettes ownership analysis")
mass_agencies = df[df['State'] == 'MA'] #looks at all the states and only chooses the ones that are MA
print(f"Total MA agencies: {len(mass_agencies)}") #how many MA agencies are we working with

print(f"\nOwnership type distribution:")
print(mass_agencies['Type of Ownership'].value_counts()) #how many MA agencies are either Gov operate, non profit, or proprietary

print(f"\nAverage star rating by ownership type in MA:")
ma_by_ownership = mass_agencies.groupby('Type of Ownership')['cleaned_patient_star_ratings'].mean() #groups MA agencies by ownership type and looks at the average star ratings for each ownership type
print(ma_by_ownership.round(2))

print(f"\nUS National averages (for comparison:)") #show national averages to compare to massachusetts averages
print(avg_by_ownership.round(2))

print("\nDetailed comparison:") #comparing each each ownership types star rating in MA to the national averages star rating 
print(f"MA NONPROFIT: {ma_by_ownership.get('NON-PROFIT', 'N/A'):.2f} vs National: {avg_by_ownership['NON-PROFIT']:.2f}")
print(f"MA Proprietary: {ma_by_ownership.get('PROPRIETARY', 'N/A'):.2f} vs National: {avg_by_ownership['PROPRIETARY']:.2f}")
print(f"MA Government: {ma_by_ownership.get('GOVERNMENT OPERATED', 'N/A'):.2f} vs National: {avg_by_ownership['GOVERNMENT OPERATED']:.2f}")

print("\nKey insights:") #showing insights for clarity
print("\nMA is 83% proprietary ({237}/{284}) vs national mix")
print(f"\nSince MA's proprietary agencies under perform national averages")
print(f"\nThe heavy proprietary concentration drags down MA's overall rating")

print("\nNational ownership distribution (%):") 
national_avg_percent = df['Type of Ownership'].value_counts(normalize=True) * 100 #taking the national average of each ownership type and converting to a percentage
print(national_avg_percent.round(1))

print(f"\nMA ownership distribution (%)")
ma_ownership_percent = mass_agencies['Type of Ownership'].value_counts(normalize=True) * 100 #same thing here with MA averages of each ownership type
print(ma_ownership_percent.round(1))

print("\nrevised insight") #revised, proprietary underperformance 
print(f"\nnational proprietary average is {avg_by_ownership['PROPRIETARY']:.2f}") 
print(f"\nMA proprietary average is {ma_by_ownership['PROPRIETARY']:.2f}")
avg_by_ownership_diff = avg_by_ownership['PROPRIETARY'] - ma_by_ownership['PROPRIETARY'] #take the difference in the national avg by ownership and MA avg by ownership
print(f"\nMA underperforms by {avg_by_ownership_diff:.2f} stars") 
print(f"\nwith 83 percent (237 of 284) of MA agencies being proprietary")
print(f'\nthe {avg_by_ownership_diff:.2f} star difference has a major impact on MA efficiency or quality, hence why the overall rating is so low.') 

print(f"\nQuantifying the impact")
proprietary_impact = avg_by_ownership_diff * (237/284) #calculating how much the proprietary rating brings down MA's overall star rating
print(f"\nthe proprietary deficit drags MA's overall rating down by approximately {proprietary_impact:.2f} stars")

ma_current = 2.98 #MA overall star rating by all ownership types
ma_if_fixed = ma_current + proprietary_impact #calculating the MA star rating if MA's star rating matched the national average star rating
print(f"\n if MA proprietary averages matched the national average, then MA would jump from {ma_current} to {ma_if_fixed:.2f}")

print(f"\nranking impact")
print(f"\nwhere would MA be ranked if they had a 3.31 rating")
total_states = df['State'].nunique()
print(f"\ntotal states: {total_states}")

states_below_ma = (avg_by_state < 2.98).sum()
current_rank = total_states - states_below_ma
print(f"\nMas current ranking: {current_rank} out of {total_states}")

states_below_331 = (avg_by_state < 3.31).sum()
new_rank= total_states - states_below_331
print(f'\nIf MA improved to 3.31: {new_rank} out of {total_states}')

improvement = current_rank - new_rank
print(f"\nthats a {improvement} position jump")

print("\n" + "-"*60)
print(f"\nFinal Summary")
print("\n" + "-"*60)

print(f"""
1. Natiional Overview:
Analyzed {len(df):,} home health agencies across {df['State'].nunique()} states/territories
National average quality: {cleaned_patient_star_ratings.mean():.2f} stars
{cleaned_patient_star_ratings.notna().sum():,} agencies with ratings ({cleaned_patient_star_ratings.notna().sum()/len(df)*100:.1f}%)

2. OWNERSHIP PERFORMANCE:
NON-PROFIT:    {avg_by_ownership['NON-PROFIT']:.2f} stars (BEST)
PROPRIETARY:   {avg_by_ownership['PROPRIETARY']:.2f} stars
GOVERNMENT:    {avg_by_ownership['GOVERNMENT OPERATED']:.2f} stars (WORST)
Gap: {avg_by_ownership['NON-PROFIT'] - avg_by_ownership['GOVERNMENT OPERATED']:.2f} stars between best and worst

3. GEOGRAPHIC PATTERNS:
Best state:  {avg_by_state.idxmax()} ({avg_by_state.max():.2f} stars)
Worst state: {avg_by_state.idxmin()} ({avg_by_state.min():.2f} stars)
Range: {avg_by_state.max() - avg_by_state.min():.2f} star difference

4. MASSACHUSETTS DEEP DIVE:
Current rank: #45 out of 55 (bottom 20%)
Root cause: Proprietary agencies underperform by {avg_by_ownership_diff:.2f} stars
Impact: 83% proprietary composition = {proprietary_impact:.2f} star drag on overall rating
Opportunity: If fixed, MA would jump to rank #25 (20-position improvement)

5. POLICY IMPLICATIONS:
Southeast states dominate top rankings (SC, AL, TN)
Mountain West states struggle (WY, MT, NV)
Wealth does not equl Quality (MA ranks below MS, AL)
Proprietary agency performance varies significantly by state
""")

