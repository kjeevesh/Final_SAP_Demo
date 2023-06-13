import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField, Button } from '@material-ui/core';

const MyComponent = () => {
  const [table1Data, setTable1Data] = useState([
    { id: 1, cells: ['Event_ID', 'Program name']  },
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

  const handleRowSelection = (row, tableNumber) => {
    if (tableNumber === 1) {
      setSelectedRow1(row);
    } else if (tableNumber === 2) {
      setSelectedRow2(row);
    }
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();

    /*{const jsonData = {
      row1: selectedRow1,
      row2: selectedRow2,
      startTime: startTime,
      interval: interval,
    };}*/

    const jsonData = {
        "list of controls":
        [
            {
                "control_1":selectedRow1,
                "control_2":selectedRow2


            }
        ],
        "list_of_servers":
        [
            {
                "username":"<username>",
                "password":"<password>",
                "ashost":"<ashost>",
                "system_number":"system_number",
                "client_no":"client_no",

            }
        ],

        scheduled_startTime: startTime,
        scheduled_Interval: interval,


    }

    console.log(jsonData);
    // You can perform further operations with jsonData (e.g., send it to a server)

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
                  style={{ backgroundColor: selectedRow1 === row ? 'blue' : 'transparent' }}
                >
                  {row.cells.map((cell, index) => (
                    <TableCell key={index}>{cell}</TableCell>
                  ))}
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
                  style={{ backgroundColor: selectedRow2 === row ? 'blue' : 'transparent' }}
                >
                  {row.cells.map((cell, index) => (
                    <TableCell key={index}>{cell}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
<br />
<br />

<h4>Scheduler</h4>
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
<br />
        <Button variant="contained" color="primary" type="submit">
          Submit
        </Button>
      </form>
    </div>
  );
};

export default MyComponent;
