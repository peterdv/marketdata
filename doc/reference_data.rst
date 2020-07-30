.. -*- coding: utf-8; mode: rst; -*-

   
.. For the Python documentation, 
   this convention is used which you may follow:
    • # with overline, for parts
    • * with overline, for chapters
    • =, for sections
    • -, for subsections
    • ^, for subsubsections
    • ", for paragraphs

Reference Data
==============

*Reference data* is a catch all term used in the finance industry to describe 
counterparty and security identifiers. 

As opposed to *market data*, the reference data is used to 
complete financial transactions and settle those transactions. 

At its most basic level, 
reference data for a simple sale of a stock in exchange for cash 
on a highly liquid stock exchange 
that involves a standard label for the underlying security (e.g., its :term:`ISIN`), 
the identity of the seller, the buyer, the broker-dealer(s), the price, etc. 

Types of data:

* Market identification
  (e.g., :term:`ISO 10383 MIC`).
* Instrument identification
  (e.g., :term:`ISIN`).
* Instrument classification 
  (e.g., large vs small, tenor, region, sector).
* Transaction information, which typically can be repressented as 
  identification data combined with a set of relations to 
  various reference data, i.e.,:

  * Transaction identifier.
  * Liquidity provider (or brooker, if you like).
  * Date and time.
  * Market.
  * Instrument.
  * Seller identity. 
  * Buyer identity. 
  * Currency (i.e., :term:`Currency Code`.
  * Quantity.
  * Price.
