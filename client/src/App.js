import { useEffect, useState } from "react";
import "./App.css";
import useDebounce from "./hook/useDebounce";
import Box from "@mui/material/Box";
import TextField from "@mui/material/TextField";
import axios from "axios";

function App() {
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const debouncedSearchTerm = useDebounce(searchTerm, 500);

  useEffect(
    () => {
      if (debouncedSearchTerm) {
        setLoading(true);
        axios
          .get(
            `http://localhost:8000/google/index/?search=${debouncedSearchTerm}`
          )
          .then((response) => {
            if (response.data) {
              setLoading(false);
              setSearchResults(response.data);
            } else {
              setSearchResults([]);
            }
          })
          .catch((error) => console.log("api errors:", error));
      } else {
        setSearchResults([]);
      }
    },
    [debouncedSearchTerm] // Only call effect if debounced search term changes
  );

  return (
    <div className="App">
      <Box
        component="form"
        sx={{
          "& > :not(style)": { m: 1 },
        }}
        noValidate
        autoComplete="off"
      >
        <TextField
          label="Search text files"
          variant="outlined"
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        {loading && <div>Searching...</div>}
        <div>
          <ol
            style={{
              textAlign: "left",
              margin: "0 0 6px 35em",
              padding: "4px 8px",
            }}
          >
            {" "}
            <h1>Search Results</h1>
            {searchResults.map((item) => {
              return (
                <li>
                  &emsp;<b>{item.words}</b> &emsp;{" "}
                  <em>
                    <u>{item.documents}</u>{" "}
                  </em>{" "}
                  <sup>{item.occurrences}</sup>
                </li>
              );
            })}
          </ol>
        </div>
      </Box>
    </div>
  );
}

export default App;
