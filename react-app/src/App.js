import React, { useState } from 'react';
// import Flatpickr from 'react-flatpickr';
import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';
import 'flatpickr/dist/themes/dark.css';
import './filters.css';
// import Box from '@mui/material/Box';

const FilterPage = () => {
  const [filters, setFilters] = useState({
    companyLocation: '',
    employeesRange: [1, 10001],
    visitorsMin: '',
    visitorsMax: '',
    // fundingMin: '',
    // fundingMax: '',
    lastFundingDate: '',
    fundingType: [],
    amountMin: '',
    amountMax: '',
    totalMin: '',
    totalMax: '',
  });

  const [prospects, setProspects] = useState({
    companies: [],
    employees: [],
  });

  const resetFilters = () => {
    // Reset filter state to initial values
    setFilters({
      companyLocation: '',
      employeesRange: [1, 10001],
      visitorsMin: '',
      visitorsMax: '',
      // fundingMin: '',
      // fundingMax: '',
      lastFundingDate: '',
      fundingType: [],
      amountMin: '',
      amountMax: '',
      totalMin: '',
      totalMax: '',
    });

    // updateDropdownOptions('company-dropdown', [], 'Prospective Companies');
  };


  const handleFilterChange = (filterName, value) => {
    setFilters((prevFilters) => ({ ...prevFilters, [filterName]: value }));
  };
  
    // useEffect(() => {
    //   // Trigger the handlePostData function when filters change
    //   handlePostData();
    // }, [postData]);

  const applyFilters = async () => {
    try {
      const response = await fetch('/prospects', 
      {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify(filters),
      });

      if (response.ok) {
        console.log('POST request successful');
        const result = await response.json();
        setProspects(result);
      } 
      else { console.error('Failed to send data'); }
    }

    catch (error) {
      console.error('Error:', error);
    }

    // const filteredCompanies = prospects.companies;
    updateDropdownOptions('company-dropdown', prospects.companies, 'Prospective Companies');
    console.log(filters);

  };

  const updateDropdownOptions = (dropdownId, options, default_Text = "") => {
    const dropdown = document.getElementById(dropdownId);

    // Clear existing options
    dropdown.innerHTML = '';

    // Add default option
    const defaultOption = document.createElement('option');
    defaultOption.disabled = true;
    defaultOption.selected = true;
    defaultOption.textContent = default_Text ;
    dropdown.appendChild(defaultOption);
    
    if (options.length === 0) { return; }
    // Add filtered options
    options.forEach((option) => {
      const newOption = document.createElement('option');
      newOption.value = option['name'];
      newOption.textContent = option['name'];
      dropdown.appendChild(newOption);
    });
  };

  // ... (Previous code)

  return (
    <div className="filter-container">
      <div className='sticky-panel'>
      <div className="left-panel">

        {/* Filter and Reset buttons */}
        <div className="filter-row">
          <button onClick={applyFilters}>Filter</button>
          <button onClick={resetFilters}>Reset</button>
        </div>


        {/* Company Location */}
        <div className="filter-row">
          <label htmlFor="company-location">Company Location</label>
          <input
            type="text"
            id="company-location"
            value={filters.companyLocation}
            onChange={(e) => handleFilterChange('companyLocation', e.target.value)}
          />
        </div>


        {/* Number of Employees Range (Slider) */}
        <div className="filter-row">
          <label>Number of Employees</label>
          <Slider
            min={1}
            max={10001}
            step={50}
            range
            style={{marginLeft: '5px', width: '85%'}}
            value={filters.employeesRange}
            onChange={(value) => handleFilterChange('employeesRange', value)}
          />
          <div className='slider-labels-container'>
            <label htmlFor='min-employees' className='slider-label-min'>{filters.employeesRange[0]}</label>
            <label htmlFor='max-employees' className='slider-label-max'>{filters.employeesRange[1]}</label>
          </div>
        </div>

        
        {/* Website Visitors Range */}
        <div className="filter-row">
          <label htmlFor="visitors-range">Website Visits / Month</label>
          <input
            type="number"
            id="visitors-Min"
            placeholder="Min"
            value={filters.visitorsMin}
            onChange={(e) => handleFilterChange('visitorsMin', e.target.value)}
          />
          <input
            type="number"
            id="visitors-Max"
            placeholder="Max"
            value={filters.visitorsMax}
            onChange={(e) => handleFilterChange('visitorsMax', e.target.value)}
          />
        </div>


        {/* Last Funding Date (Radio Buttons) */}
        <div className="filter-row">
          <label>Last Funding Date</label>
          <div>
            {['past1Month', 'past3Months', 'past6Months', 'past9Months', 'past1Year'].map((option) => (
              <div key={option}>
                <input
                  type="radio"
                  id={`last-funding-${option}`}
                  value={option}
                  checked={filters.lastFundingDate === option}
                  onChange={() => handleFilterChange('lastFundingDate', option)}
                />
                <label htmlFor={`last-funding-${option}`} className="radio-button-label">
                  {option.replace('past', 'Past ').replace('Months', ' Months').replace('Year', ' Year')}
                </label>
              </div>
            ))}
          </div>
        </div>

        {/* Last Funding Date Range */}
        {/* <div className="filter-row">
          <label htmlFor="last-funding-date">Last Funding Date:</label>
          <Flatpickr
            value={filters.fundingMin}
            onChange={(date) => handleFilterChange('fundingMin', date[0])}
            placeholder="Min"
          />
          <Flatpickr
            value={filters.fundingMax}
            onChange={(date) => handleFilterChange('fundingMax', date[0])}
            placeholder="Max"
          />  
        </div> */}


        {/* Last Funding Type (Checkbox Buttons) */}
        <div className="filter-row">
          <label>Last Funding Type</label>
          <div>
            {['Series A', 'Series B', 'Series C', 'Series D', 'Series E - G',  'Series H - J', 'Seed', 'Angel', 'Private Equity'].map((option) => (
              <div key={option}>
                <input
                  type="checkbox"
                  id={`funding-type-${option}`}
                  checked={filters.fundingType.includes(option)}
                  onChange={() => handleFilterChange('fundingType', toggleCheckbox(filters.fundingType, option))}
                />
                <label htmlFor={`funding-type-${option}`} className = "check-box-label">{option}</label>
              </div>
            ))}
          </div>
        </div>


        {/* Last Funding Amount Range */}
        <div className="filter-row">
          <label htmlFor="last-funding-amount">Last Funding Amount</label>
          <input
            type="number"
            id="amount-Min"
            placeholder="Min"
            value={filters.amountMin}
            onChange={(e) => handleFilterChange('amountMin', e.target.value)}
          />
          <input
            type="number"
            id="amount-Max"
            placeholder="Max"
            value={filters.amountMax}
            onChange={(e) => handleFilterChange('amountMax', e.target.value)}
          />
        </div>


        {/* Total Funding Raised Range */}
        <div className="filter-row">
          <label htmlFor="total-funding-raised">Total Funding Raised</label>
          <input
            type="number"
            id="total-Min"
            placeholder="Min"
            value={filters.totalMin}
            onChange={(e) => handleFilterChange('totalMin', e.target.value)}
          />
          <input
            type="number"
            id="total-Max"
            placeholder="Max"
            value={filters.totalMax}
            onChange={(e) => handleFilterChange('totalMax', e.target.value)}
          />
        </div>


      </div>
      </div>


      <div className="center-panel">
        
        <div class="company-list">
          <select id="company-dropdown">
            <option disabled selected>Prospective Companies</option>
          </select>
        </div>

        <div class="employee-list">
          <select id="employee-dropdown">
            <option disabled selected>Prospective Employees</option>
          </select>
        </div>

      </div>


    </div>
  );

};

export default FilterPage;

function toggleCheckbox(arr, value) {
  if (arr.includes(value)) {
    return arr.filter((item) => item !== value);
  } else {
    return [...arr, value];
  }
} 