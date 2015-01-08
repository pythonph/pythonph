var React = require('react/addons');
var superagent = require('superagent');

var Job = React.createClass({
  getInitialState: function() {
    return {
      toggled: false
    };
  },
  toggleDetails: function() {
    this.setState({toggled: !this.state.toggled});
  },
  renderDetails: function() {
    return this.state.toggled ? (
      <div className="details">
        <p className="description">{this.props.description}</p>
        <p>
          <a
            className="apply button"
            href={this.props.application_url}
          >
            Apply for this job
          </a>
        </p>
      </div>
    ) : null;
  },
  render: function() {
    return (
      <li>
        <div className="row">
          <div className="two-thirds column">
            <h2>
              <a href="#" onClick={this.toggleDetails}>
                {this.props.title}
              </a>
            </h2>
            <span className="location">{this.props.location}</span>
            {this.renderDetails()}
          </div>
          <div className="one-third column">
            <h3>{this.props.company.name}</h3>
            <span className="user">
              Posted by {this.props.user.name}
            </span>
          </div>
        </div>
      </li>
    );
  }
});

module.exports = React.createClass({
  displayName: 'Jobs',
  getInitialState: function() {
    return {
      jobs: null,
      next: null,
      prev: null
    };
  },
  apiUrl: function() {
    return ['/api', this.props.apiVersion].concat(
      Array.prototype.slice.call(arguments)
    ).join('/');
  },
  componentDidMount: function() {
    superagent
      .get(this.apiUrl('job'))
      .end(this.parseJobs);
  },
  parseJobs: function(res) {
    this.setState({
      jobs: res.body.objects,
      next: res.body.meta.next,
      prev: res.body.meta.previous
    });
  },
  renderJob: function(data) {
    return <Job key={data.id} {...data} />
  },
  renderJobs: function() {
    return this.state.jobs ? (
      this.state.jobs.length > 0 ? (
        this.state.jobs.map(this.renderJob)
      ) : (
        <li>No jobs has been posted yet.</li>
      )
    ) : (
      <li>Loading jobs&hellip;</li>
    );
  },
  prevJobs: function() {
    if (this.state.prev) {
      this.setState({jobs: null});
      superagent
        .get(this.state.prev)
        .end(this.parseJobs);
    }
  },
  nextJobs: function() {
    if (this.state.next) {
      this.setState({jobs: null});
      superagent
        .get(this.state.next)
        .end(this.parseJobs);
    }
  },
  render: function() {
    return (
      <div>
        <ul className="jobs">
          {this.renderJobs()}
        </ul>
        <div className="pagination u-full-width u-cf">
          <button
            className="u-pull-left"
            onClick={this.prevJobs}
            disabled={!this.state.prev}
          >
            Previous
          </button>
          <button
            className="u-pull-right"
            onClick={this.nextJobs}
            disabled={!this.state.next}
          >
            Next
          </button>
        </div>
      </div>
    );
  }
});
