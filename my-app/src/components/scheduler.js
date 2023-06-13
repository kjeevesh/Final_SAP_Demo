import React, { useState } from 'react';
import TableTwo from './tabletwo';
import TableOne from './tableone';
import Form from './form';
import './styles.css';
import BasicDateTimePicker from './datetime';


const Scheduler = () => {

  const handleSubmitone = (startTime, endTime, selectedRows) => {

    const jsonData = {
      selectedRowsTableOne,
      selectedRowsTableTwo,
      startTime,
      endTime,
    };

    console.log(jsonData); // or send the data to an API endpoint

    // lear the form or perform any other necessary actions
    setSelectedRowsTableOne(null);
    setSelectedRowsTableTwo(null);
    
  };

  const [selectedRowsTableOne, setSelectedRowsTableOne] = useState([]);
  const [selectedRowsTableTwo, setSelectedRowsTableTwo] = useState([]);

  const handleRowClick = (rowId, tableName) => {
    if (tableName === 'TableOne') {
      const isSelected = selectedRowsTableOne.includes(rowId);
      if (isSelected) {
        setSelectedRowsTableOne(selectedRowsTableOne.filter(id => id !== rowId));
      } else {
        setSelectedRowsTableOne([...selectedRowsTableOne, rowId]);
      }
    } else if (tableName === 'TableTwo') {
      const isSelected = selectedRowsTableTwo.includes(rowId);
      if (isSelected) {
        setSelectedRowsTableTwo(selectedRowsTableTwo.filter(id => id !== rowId));
      } else {
        setSelectedRowsTableTwo([...selectedRowsTableTwo, rowId]);
      }
    }
  };

  return (
    <div>
      
      <br />
      

      <TableOne handleRowClick={handleRowClick} />
      <br />
      
      <TableTwo handleRowClick={handleRowClick} />
      <br />

      <h4>Scheduler</h4>
      <br />
      
      <BasicDateTimePicker />
      <br />

      
    </div>
  );
};

export default Scheduler