import 'bootstrap/dist/css/bootstrap.min.css';
import BasicExample from './components/header';
import Scheduler from './components/scheduler';
import { BrowserRouter, Switch, Route } from "react-router-dom";
import MyComponent from './components/mycomponents';

function App() {
  return (
    <BrowserRouter>
    <Switch>
      <Route exact path="/" component={BasicExample} />
      <Route path="/scheduler" component={Scheduler} />
      <Route path="/SAP-Monitoring" component={MyComponent} />
      <Route path="/home" component={BasicExample} />
      <Route path="/SAP" component={Scheduler} />
    </Switch>
  </BrowserRouter>
  );
}

export default App;
