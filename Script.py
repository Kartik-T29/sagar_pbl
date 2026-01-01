# Install dependencies as needed:
# pip install kagglehub[pandas-datasets]
import kagglehub
from kagglehub import KaggleDatasetAdapter

df = kagglehub.dataset_load(
  KaggleDatasetAdapter.PANDAS,
  "asaniczka/tmdb-movies-dataset-2023-930k-movies",
  path = 'TMDB_movie_dataset_v11.csv'

)

print("First 5 records:", df.head(5))