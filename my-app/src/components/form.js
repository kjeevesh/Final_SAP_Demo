import React, { useState } from 'react';
import './styles.css'


const Form = ({ handleSubmitone }) => {
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');

  const handleStartTimeChange = (event) => {
    setStartTime(event.target.value);
  };

  const handleEndTimeChange = (event) => {
    setEndTime(event.target.value);
  };

  const handleSubmitClick = () => {
    handleSubmitone(startTime, endTime);
  };

  return (
    <div className="form-container">
      <h2>Scheduler</h2>
      <form className="time-form">
        <div className="form-group">
          <label htmlFor="startTime">Start Time (UTC)</label>
          <input
            type="text"
            id="startTime"
            className="form-control"
            value={startTime}
            onChange={handleStartTimeChange}
          />
        </div>
        <div className="form-group">
          <label htmlFor="endTime">End Time (UTC)</label>
          <input
            type="text"
            id="endTime"
            className="form-control"
            value={endTime}
            onChange={handleEndTimeChange}
          />
        </div>
        <button type="button" className="submit-btn" onClick={handleSubmitClick}>
          Submit
        </button>
      </form>
    </div>
  );
};

export default Form;
