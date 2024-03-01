import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './styles/App.css';

var kCurrentTable = "users";
var kOutput = [];
var kFormFields = []

const App = () => {
  const [formFields, setFormFields] = useState([]); // List of input field names
  const [output, setOutput] = useState([]); // List of output for table

  useEffect(() => {
    fetchFormInputs()
    getData()
  }, [])

   // Update input fields and table results with new table
   const fetchFormInputs = async () => {
    await axios.get(
      "http://localhost:8080/api/users/columns"
    )
    .then((res) => {
      kFormFields = res.data["table_columns"]
    })
    .catch((err) => {
      console.error(err)
    })    
    setFormFields(kFormFields)
    console.log(kFormFields)
  }

  // Format response JSON into list
  const getData = async () => {
    await axios.get(
      `http://localhost:8080/api/users`
    )
    .then((res) => {
      kOutput = []
      let results = res.data["records"];
      for (let i = 0; i < results.length; ++i) {
        let out = []
        for (let j = 0; j < kFormFields.length; ++j) {
          out.push(results[i][kFormFields[j]])
        }
        kOutput.push(out)
      }
    })
    .catch((err) => {
      console.error(err)
    })
    setOutput(kOutput)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    var formInputs = {};
    let contains = false;
    formInputs["data"] = {}
    for (let i = 0; i < formFields.length; ++i) {
      formInputs["data"][formFields[i]] = e.target[i].value;
    }
    for (let i = 0; i < kOutput.length; ++i) {
      contains = contains || kOutput[i].includes(formInputs["data"]["id"]);
    }
    console.log(contains)
    if (contains) {
      await axios.put(
        `http://localhost:8080/api/users/${formInputs["data"]["id"]}`,
        formInputs
      )
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => {
        console.error(err)
      })
    }
    else {
      await axios.post(
        `http://localhost:8080/api/users/${formInputs["data"]["id"]}`,
        formInputs
      )
      .then((res) => {
        console.log(res.data)
      })
      .catch((err) => {
        console.error(err)
      })
    }
    getData()
  }

  const deleteEntry = async (e) => {
    console.log(e[0])

    await axios.delete(
      `http://localhost:8080/api/users/${e[0]}`
    )
    .then((res) => {
      console.log(res.data)
    })
    .catch((err) => {
      console.error(err)
    })
    getData()
  }

  const getEntry = async(e) => {
    console.log(e.target[0].value)
    e.preventDefault()
    await axios.get(
      `http://localhost:8080/api/users/${e.target[0].value}`
    )
    .then((res) => {
      console.log(res.data["records"])
      alert(`name: ${res.data["records"][0]["name"]}\npoints: ${res.data["records"][0]["points"]}`)
    })
    .catch((err) => {
      alert(`User ID not found`)
    })
    getData()
  }

  return (
    <div className="App">
      <header className="App-header">
      <h2>Instructions: New ids will post to the database, existing ids will put to the database. Search below, click X to exit.</h2>
        <form onSubmit={(e) => handleSubmit(e)}>
          <h3> {kCurrentTable} Table Form </h3>
          <ul style={{listStyleType:"none"}}>
            {formFields.map((item, index) => (
              <li key={index}>
                <label style={{marginRight:"20px"}}>{item}</label>
                <input
                  required
                  type="text"
                />
                <br/>
              </li>
            ))}
          </ul>
          <button type="submit">Submit</button>
        </form>
        <h3>users Table Entries</h3>
        <table>
          <thead>
            <tr>
              <th></th>
              {formFields.map((item, index) => (
                <th key={index}>{item}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {output.map((item, index) => {
              return (
                <tr key={index}>
                  <button onClick={() => deleteEntry(item)} style={{marginRight:"10px"}}>X</button>
                  {item.map((it, ix) => {
                    return (
                    <td key={ix}>{it}</td>
                    )
                  })}
                </tr>
              )
            })}
          </tbody>
        </table>
        <form onSubmit={(e) => getEntry(e)} style={{marginBottom:"50px"}}>
          <h3>Find User By Id</h3>
          <label style={{marginRight:"20px"}}>id</label>
          <input
            required
            type="text"
          />
          <button type="submit" style={{marginLeft:"10px"}}>Submit</button>
        </form>
      </header>
    </div>
  );
}

export default App;
