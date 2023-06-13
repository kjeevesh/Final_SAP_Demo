import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField, Button } from '@material-ui/core';
const ApiMyComponent = () => {
    const [table1Data, setTable1Data] = useState([
      { id: 1, cells: ['Event_ID', 'Program name'] },
      { id: 2, cells: ['BUS001', 'ZBUS001'] },
      { id: 3, cells: ['ITSEC001', 'ZITSEC001' ]},
      { id: 4, cells: ['MC_MM_P033', 'ZMC_MM_P033'] },
      { id: 5, cells: ['MC_MM_P033', 'ZMC_MM_P033'] },
    ]);
  
    const [table2Data, setTable2Data] = useState([
      { id: 1, cells: ['Event_ID', 'Program name'] },
      { id: 2, cells: ['BUS001', 'ZBUS001'] },
      { id: 3, cells: ['ITSEC001', 'ZITSEC001'] },
      { id: 4, cells: ['MC_MM_P033', 'ZMC_MM_P033'] },
      { id: 4, cells: ['MC_MM_P033', 'ZMC_MM_P033'] },
    ]);
  
  const [selectedRow1, setSelectedRow1] = useState(null);
  const [selectedRow2, setSelectedRow2] = useState(null);
  const [startTime, setStartTime] = useState('');
  const [interval, setInterval] = useState('');
  const [responseData, setResponseData] = useState(null);

  const handleRowSelection = (row, tableNumber) => {
    if (tableNumber === 1) {
      setSelectedRow1(row);
    } else if (tableNumber === 2) {
      setSelectedRow2(row);
    }
  };

  const handleFormSubmit = async (e) => {
    e.preventDefault();

    const jsonData = {
      row1: selectedRow1,
      row2: selectedRow2,
      startTime: startTime,
      interval: interval,
    };

    try {
      alert('hi')
      const response = fetch('http://127.0.0.1:5000/api/submitData', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
      });


      const jsonData = {
        row1: selectedRow1,
        row2: selectedRow2,
        startTime: startTime,
        interval: interval,
      };

    

      if (response.ok) {
        const responseData = await response.json();
        setResponseData(responseData); // Store the response data in state
      } else {
        console.log('Error:', response.status);
      }
    } catch (error) {
      console.log('Error:', error);
    }

    // Reset the form
    setSelectedRow1(null);
    setSelectedRow2(null);
    setStartTime('');
    setInterval('');
  };

  return (
    <div>
      <form onSubmit={handleFormSubmit}>
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Table 1</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {table1Data.map((row) => (
                <TableRow
                  key={row.id}
                  onClick={() => handleRowSelection(row, 1)}
                  style={{ backgroundColor: selectedRow1 === row ? 'yellow' : 'transparent' }}
                >
                  <TableCell>{row.name}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Table 2</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {table2Data.map((row) => (
                <TableRow
                  key={row.id}
                  onClick={() => handleRowSelection(row, 2)}
                  style={{ backgroundColor: selectedRow2 === row ? 'yellow' : 'transparent' }}
                >
                  <TableCell>{row.info}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>

        <TextField
          label="Start Time"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          variant="outlined"
        />

        <TextField
          label="Interval"
          value={interval}
          onChange={(e) => setInterval(e.target.value)}
          variant="outlined"
        />

        <Button variant="contained" color="primary" type="submit">
          Submit
        </Button>
      </form>

      {responseData && (
        <div>
          <h3>Response Data:</h3>
          <pre>{JSON.stringify(responseData, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default ApiMyComponent;
