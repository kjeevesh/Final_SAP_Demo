import * as React from 'react';
import dayjs from 'dayjs';
import { DemoContainer } from '@mui/x-date-pickers/internals/demo';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';

import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { SingleInputDateTimeRangeField } from '@mui/x-date-pickers-pro/SingleInputDateTimeRangeField';
import { Button } from '@material-ui/core';

export default function DateTimeRangeFieldValue() {
  const handleClick = () => {
    window.alert("Job Scheduled Successfully");
  };
  const [value, setValue] = React.useState(() => [
    dayjs('2022-04-17T15:30'),
    dayjs('2022-04-21T18:30'),
  ]);

  return (
    <><LocalizationProvider dateAdapter={AdapterDayjs}>
      <DemoContainer
        components={[
          'SingleInputDateTimeRangeField',
          'SingleInputDateTimeRangeField',
        ]}
      >
        <SingleInputDateTimeRangeField
          label="Start Time"
          defaultValue={[dayjs('2022-04-17T15:30'), dayjs('2022-04-21T18:30')]} />
        
        <SingleInputDateTimeRangeField
          label="End Time"
          value={value}
          onChange={(newValue) => setValue(newValue)} />
      </DemoContainer>
      </LocalizationProvider><Button variant="contained" color="primary" onClick={handleClick}>Submit</Button></>
  );
}